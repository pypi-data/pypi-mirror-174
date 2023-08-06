# -*- coding: utf-8 -*-
import json


class JsonConvert(object):
    @staticmethod
    def __encode(o):
        if hasattr(o, '__dict__'):
            return o.__dict__

    @staticmethod
    def load(s):
        return json.loads(s, encoding='utf-8')

    @staticmethod
    def format(o):
        return json.dumps(o, default=JsonConvert.__encode)


def isNullOrEmpty(str):
    if str is None or str == '':
        return True
    return False
