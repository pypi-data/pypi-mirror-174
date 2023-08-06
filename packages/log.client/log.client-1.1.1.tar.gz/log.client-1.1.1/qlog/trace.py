#!/usr/bin/env python
# -*- coding: utf-8 -*-

' module comments'
import threading

import qlog.logger

__author__ = 'dugangandy@qq.com'


class Tracer(object):
    def __init__(self):
        self.stack = []

    def newSpan(self, topic, title):
        span = qlog.logger._SpanLog(topic, title)
        if self.stack.__len__() > 0:
            pSpan = self.stack[-1]
            span.parentSpanId = pSpan.spanId
            span.requestId = pSpan.requestId
            span.traceId = pSpan.traceId
            span.spanDepth = pSpan.spanDepth + 1
        self.stack.append(span)
        return span

    def peek(self):
        if self.stack.__len__() > 0:
            return self.stack[-1]
        return qlog.logger._NullSpan()


def getCurrent():
    _threadLocal = threading.local()
    if not hasattr(_threadLocal, 'tracer'):
        _threadLocal.tracer = Tracer()
    return _threadLocal.tracer
