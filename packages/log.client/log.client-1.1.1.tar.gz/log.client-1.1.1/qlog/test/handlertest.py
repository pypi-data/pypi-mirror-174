# -*- coding: utf-8 -*-
import logging
import logging.config
from time import sleep
from unittest import TestCase


import qlog.trace


class LogTests(TestCase):
    def setUp(self):
        logging.config.fileConfig('logging.ini')

    def tearDown(self):
        pass

    def test_log(self):
        tracer = qlog.trace.getCurrent()
        span1 = tracer.newSpan('/api/zoo/1', 'post')
        span1.tag = 'rpc.server'
        span = tracer.newSpan('/api/zoo/1', 'get')
        span.tag = 'rpc.sucker'
        logger = logging.getLogger('root')
        logger.info('这是一条中文字符测试日志')
        logger.info('this is a info log.')
        logger.warning('this is a warning log.')
        sleep(2)
        span.finish()
        span1.finish()

        # try:
        #     n = 1 / 0
        # except Exception as e:
        #     logger.error('test error: %s', e)
        #     logger.fatal('test fatal: %s', e)
        count = 0
        for i in range(10000):
            logger.warning('test warn')
            count += 1
        print("已发送日志: {}条".format(count))

        sleep(30)
