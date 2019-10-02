#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : actanble
date   : 2018年4月11日
role   : 缓存
"""

import base64
import json

import redis
# 替换 short_uuid 为 uuid; 关闭 __salt
try:
    from shortuuid import uuid
except:
    from uuid import uuid4 as uuid
from .tools import singleton, bytes_to_unicode, convert

try:
    from xdsl.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB
except Exception as e:
    print(e)
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'sqsjywl123'
    REDIS_DB = 10


@singleton
class Cache(object):
    def __init__(self, host='localhost', port=6379,
                 db=10, password='sqsjywl123',
                 decode_responses=False):
        self.__redis_connections = {}

        auth = password
        host = host
        port = port
        db = db
        return_utf8 = False
        if decode_responses:
            return_utf8 = False
        if auth:
            redis_conn = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=return_utf8)
        else:
            redis_conn = redis.Redis(host=host, port=port, db=db, decode_responses=return_utf8)
        self.__redis_conn = redis_conn
        self.__salt = uuid()

    def set(self, key, value, expire=-1, private=False, pipeline=None):
        real_key = self.__get_key(key, private)
        execute_main = self.__get_execute_main(pipeline)
        if expire > 0:
            execute_main.set(real_key, value, ex=expire)
        else:
            execute_main.set(real_key, value)

    def get(self, key, default='', private=False, pipeline=None):
        real_key = self.__get_key(key, private)
        execute_main = self.__get_execute_main(pipeline)
        if execute_main.exists(real_key):
            result = execute_main.get(real_key)
            return bytes_to_unicode(result)
        return default

    def incr(self, key, private=False, amount=1):
        real_key = self.__get_key(key, private)
        execute_main = self.__get_execute_main()
        if execute_main.exists(real_key):
            execute_main.incr(real_key, amount=amount)
            return self.get(key, default='0', private=private)
        return None

    def set_json(self, key, value, expire=-1, private=False, pipeline=None):
        value = json.dumps(value)
        value = base64.b64encode(value.encode('utf-8'))
        self.set(key, value, expire, private, pipeline)

    def get_json(self, key, default='', private=False):
        # 修复默认参数 2019-9-16
        default = base64.b64encode(json.dumps(default).encode('utf-8'))
        result = self.get(key, default, private)
        result = base64.b64decode(result)
        result = bytes_to_unicode(result)
        if result:
            result = json.loads(result)
        return result

    def delete(self, *keys, private=False, pipeline=None):
        execute_main = self.__get_execute_main(pipeline)
        _keys = [self.__get_key(key, private) for key in keys]
        return execute_main.delete(*_keys)

    def clear(self):
        execute_main = self.__get_execute_main()
        execute_main.flushdb()

    def get_pipeline(self):
        return self.__redis_conn.pipeline()

    def execute_pipeline(self, pipeline):
        if pipeline:
            return pipeline.execute()

    def get_conn(self):
        return self.__get_execute_main()

    def hgetall(self, key, default='',  private=False):
        real_key = self.__get_key(key, private)
        execute_main = self.__get_execute_main()
        if execute_main.exists(real_key):
            result = execute_main.hgetall(real_key)
            result = convert(result)
        else:
            return default
        return result

    @property
    def redis(self):
        return self.__get_execute_main()

    def __get_key(self, key, private=False):
        if private:
            return '%s%s' % (self.__salt, key)
        else:
            return key

    def __get_execute_main(self, pipeline=None):
        if pipeline:
            return pipeline
        return self.__redis_conn


def get_cache():
    return Cache(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)


cache = get_cache()