# coding:utf-8
import json
# from xdsl.test import test_insert_example
from elasticsearch.helpers import bulk

from xdsl.parse import parse_nginx_log_item
from xdsl.modles import NginxAccessLog, client
from xdsl.opssdk.cache import cache
from xdsl.settings import NGX_MAX_INSERT_NUM, NGX_REDIS_RESULTS_KEY, DELAY_EXP, DELAY_EXP_KEY1, \
    SOURCE_IP_KEY, HOST_FORM_KEY
from xdsl.opssdk.ops_logs import ins_log as logging


class Py3AccessDest4Es(object):

    @staticmethod
    def cache_inital():
        cache.set_json(NGX_REDIS_RESULTS_KEY, [])
        cache.set(DELAY_EXP_KEY1, 'ANY_VALUE', DELAY_EXP)

    def send(self, msg):
        """
        步骤说明：
           批量插入的原理探究;
             - 条件： 要么够了 max_insert_num 或者 延迟的时间到了 delay_exp
             - 第一次进来肯定是空。那么直接一次插入一条。
        :param msg:
        :return:
        """
        item = json.loads(str(bytes.decode(msg['LEGACY_MSGHDR'] + msg['MESSAGE'], 'utf-8')))

        if not cache.get(SOURCE_IP_KEY):
            cache.set(SOURCE_IP_KEY, str(msg['SOURCEIP']))
        if not cache.get(HOST_FORM_KEY):
            cache.set(HOST_FORM_KEY, str(msg['HOST_FROM']))

        inserted = cache.get_json(NGX_REDIS_RESULTS_KEY)
        if not inserted:
            cache.set_json(NGX_REDIS_RESULTS_KEY, [])
            inserted = []
        expired = cache.get(DELAY_EXP_KEY1)
        count_inserted = len(inserted)
        if count_inserted > NGX_MAX_INSERT_NUM or not expired:
            if count_inserted < 1:
                # 到了时间就只插入当前响应的这一条
                inserted.append(item)
            docs = []
            for x in inserted:
                _item = parse_nginx_log_item(x)
                _tmp = NginxAccessLog(meta={'id': _item["request_id"]}, **_item)
                docs.append(_tmp)
            bulk(client=client, actions=[{
                "_index": NginxAccessLog._index._name,
                "_type": "_doc",
                "_source": x
            } for x in docs])
            logging.info('批量插入【{}】条nginx_access记录到Es数据库!'.format(str(len(docs))))
            Py3AccessDest4Es.cache_inital()

        else:
            logging.info('记录到Redis数据库准备多条插入! 【 {cur} / {max}】'.format(cur=len(inserted), max=NGX_MAX_INSERT_NUM))
            inserted.append(item)
            cache.set_json(NGX_REDIS_RESULTS_KEY, inserted)
        return True


class Py3AlertDest4Es(object):

    @staticmethod
    def cache_inital():
        cache.set_json(NGX_REDIS_RESULTS_KEY, [])
        cache.set(DELAY_EXP_KEY1, 'ANY_VALUE', DELAY_EXP)

    def send(self, msg):
        item = json.loads(str(bytes.decode(msg['LEGACY_MSGHDR'] + msg['MESSAGE'], 'utf-8')))
        print(item)
        print('=======11111111=========alert=2222222============333333333========')
        return True


class Py3ErrorDest4Es(object):

    @staticmethod
    def cache_inital():
        cache.set_json(NGX_REDIS_RESULTS_KEY, [])
        cache.set(DELAY_EXP_KEY1, 'ANY_VALUE', DELAY_EXP)

    def send(self, msg):
        item = json.loads(str(bytes.decode(msg['LEGACY_MSGHDR'] + msg['MESSAGE'], 'utf-8')))
        print(item)
        print('=======11111111==33333==error==33=2222333========')
        return True
