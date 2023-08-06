# -*- coding: utf-8 -*-
import json
import random
import sys

from qlog.utils import JsonConvert

if 3 <= sys.version_info[0]:
    _PY3 = True
else:
    _PY3 = False

if _PY3:
    from queue import Queue
    import queue
else:
    print("package qlog doesn't support python 2.x now.")
    # import Queue
    # from urlparse import urljoin

import datetime
import logging
import socket
import threading
import time
import traceback
import uuid

import requests

import qlog.trace
import qlog.utils

from configparser import ConfigParser
from elasticsearch import Elasticsearch
from elasticsearch import helpers

if _PY3:
    _LogQueue = Queue(maxsize=1024 * 8)
else:
    _LogQueue = Queue.Queue(maxsize=1024 * 8)
_SECTION_NAME = 'log'
_ES_URL_KEY = 'es_urls'
_INDEX_NAME_KEY = 'es_index_name'
_APP_NAME_KEY = 'app_name'

conf = ConfigParser()
conf.read('config.ini', encoding='utf-8')

_APP_NAME = conf.get(_SECTION_NAME, _APP_NAME_KEY)
_LOG_SERVERS = conf.get(_SECTION_NAME, _ES_URL_KEY)
_APPLOG_INDEX_NAME = conf.get(_SECTION_NAME, _INDEX_NAME_KEY, fallback='application-log')

_logger = logging.getLogger(__name__)


def __get_local_addr():
    try:
        _local_ip = '127.0.0.1'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        _local_ip = s.getsockname()[0]
    except:
        pass
    finally:
        s.close()
    return _local_ip


LocalIP = __get_local_addr()


def getCurrentTimestamp():
    millis = int(round(time.time() * 1000))
    return millis


class _BaseLog(object):
    def __init__(self, topic='', title=''):
        self.ip = LocalIP
        self.id = str(uuid.uuid4())
        self.logType = 'event'
        self.appName = _APP_NAME
        self.eventId = str(threading.current_thread().ident)
        self.createDate = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+0800'
        self.finished = False

        self.className = topic
        self.methodName = title
        self.tag = ''
        self.content = ''
        self.level = 1
        self.requestId = str(uuid.uuid4())
        self.traceId = str(uuid.uuid4())
        self.parentSpanId = '-1'
        self.indexName = _APPLOG_INDEX_NAME

        self.remoteSystemAlias = ''
        self.remoteIpAddress = ''
        # self.logType = 'span'
        self.spanId = str(uuid.uuid4())
        self.spanDepth = 0
        self.metricValue = getCurrentTimestamp()
        self.valid = True

    def end(self):
        if not self.finished:
            try:
                _LogQueue.put_nowait(self)
                self.finished = True
            except queue.Full:
                print("queue is full when log end")
                pass


class _EventLog(_BaseLog):
    def __init__(self, topic='', title=''):
        super(_EventLog, self).__init__(topic, title)

    def finish(self):
        span = qlog.trace.getCurrent().peek()
        if span.valid:
            self.requestId = span.requestId
            self.traceId = span.traceId
            self.parentSpanId = span.spanId
        super(_EventLog, self).end()


class _SpanLog(_BaseLog):
    def __init__(self, topic='', title=''):
        super(_SpanLog, self).__init__(topic, title)
        self.logType = 'span'

    def finish(self):
        tracer = qlog.trace.getCurrent()
        while tracer.stack.__len__() > 0:
            s = tracer.stack.pop()
            if self == s:
                self.metricValue = getCurrentTimestamp() - self.metricValue
                super(_SpanLog, self).end()
                break


class _NullSpan(_EventLog):
    def __init__(self):
        self.valid = False
        pass

    def finish(self):
        pass


class _AppLog(_SpanLog):
    def __init__(self):
        super(_AppLog, self).__init__()
        pass


class _LogConsumer(threading.Thread):
    __MAX_COMMIT_SIZE = 16

    def __init__(self):
        super(_LogConsumer, self).__init__()
        servers = _LOG_SERVERS
        if qlog.utils.isNullOrEmpty(servers):
            raise Exception('can not get log servers')
        self.endpoints = servers.split(',')
        self.es = Elasticsearch(hosts=self.endpoints[random.randint(0, len(self.endpoints) - 1)])
        self.setDaemon(True)
        self.session = requests.Session()
        self.session.headers.update({'content-type': 'application/json'})
        self.logger = logging.getLogger('_LogstashConsumer')

    def __commit_logs(self):
        batch_size = min(_LogQueue.qsize(), _LogConsumer.__MAX_COMMIT_SIZE)
        logs = []
        if batch_size > 0:
            for i in range(batch_size):
                logs.append(_LogQueue.get())
        if logs.__len__() == 0:
            time.sleep(.01)
            return
        # endpoints = self.endpoints
        es = self.es
        try:
            # i = randint(0, len(endpoints) - 1)
            # endpoint = endpoints[i]
            data = JsonConvert.format(logs)
            actions = []
            for log in json.loads(data):
                action = {'_op_type': 'index', '_index': _APPLOG_INDEX_NAME, '_source': log}
                actions.append(action)
            helpers.bulk(client=es, actions=actions)

        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
            print(traceback.format_exc())
            self.logger.error(traceback.format_exc())
            # when connection error or timeout ,shutdown local session
            self.session.close()
            _logger.warn('connection error or timeout')
            # sleep for network recover
            time.sleep(2)
            # rebuild local session
            self.session = requests.Session()
            self.session.headers.update({'content-type': 'application/json'})
            # requeue logs
            self._reQueue(logs)

        except BaseException:
            print(traceback.format_exc())
            self.logger.warning(traceback.format_exc())
            time.sleep(2)
            # requeue logs for other problem
            self._reQueue(logs)

    def _reQueue(self, logs):
        for log in logs:
            try:
                log.finished = False
                log.finish()
            except queue.Full:
                print("queue is full when requeue")
                pass

    def run(self):
        while True:
            self.__commit_logs()


class _QLogger(object):
    def __init__(self):
        pass

    def append(self, topic, title, content, level):
        try:
            item = _EventLog()
            item.level = level
            item.content = content
            item.className = topic
            item.methodName = title
            item.finish()
        except queue.Full:
            print("queue is full when append")
            pass


class QlogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.logger = _QLogger()
        self.logConsumer = _LogConsumer()
        self.logConsumer.start()

    def emit(self, record):
        level = 0
        if record.levelno == logging.INFO:
            level = 1
        elif record.levelno == logging.WARN:
            level = 2
        elif record.levelno == logging.ERROR:
            level = 3
        elif record.levelno == logging.FATAL:
            level = 4
        self.logger.append(record.module, record.funcName, self.format(record), level)
