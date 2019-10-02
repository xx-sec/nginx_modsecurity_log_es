# coding:utf-8
import json
# from xdsl.test import test_insert_example
from elasticsearch.helpers import bulk

from xdsl.parse import parse_nginx_log_item, parse_nginx_error_mod_log, parse_nginx_alert_item
from xdsl.modles import NginxAccessLog, client, NginxAlertLog, NginxErrorLog
from xdsl.opssdk.cache import cache
from xdsl.settings import  SOURCE_IP_KEY, HOST_FORM_KEY, DELAY_EXP, \
    NGX_ACS_DELAY_EXP_KEY, NGX_ACS_MAX_INSERT_NUM, NGX_ACS_RESULTS_KEY, \
    NGX_AUD_DELAY_EXP_KEY, NGX_AUD_MAX_INSERT_NUM, NGX_AUD_RESULTS_KEY, \
    NGX_ERR_DELAY_EXP_KEY, NGX_ERR_MAX_INSERT_NUM, NGX_ERR_RESULTS_KEY

from xdsl.opssdk.ops_logs import ins_log as logging


class Py3AccessDest4Es(object):

    @staticmethod
    def cache_inital():
        cache.set_json(NGX_ACS_RESULTS_KEY, [])
        cache.set(NGX_ACS_DELAY_EXP_KEY, 'ANY_VALUE', DELAY_EXP)

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

        inserted = cache.get_json(NGX_ACS_RESULTS_KEY)
        if not inserted:
            cache.set_json(NGX_ACS_RESULTS_KEY, [])
            inserted = []
        expired = cache.get(NGX_ACS_DELAY_EXP_KEY)
        count_inserted = len(inserted)
        if count_inserted > NGX_ACS_MAX_INSERT_NUM or not expired:
            if count_inserted < 1:
                logging.info('[Access]响应时间到；准备插入单条')
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
            logging.info('[Access]批量插入【{}】条nginx_access记录到Es数据库!'.format(str(len(docs))))
            Py3AccessDest4Es.cache_inital()

        else:
            logging.info('[Access]记录到Redis数据库准备多条插入! 【 {cur} / {max}】'.format(cur=len(inserted), max=NGX_ACS_MAX_INSERT_NUM))
            inserted.append(item)
            cache.set_json(NGX_ACS_RESULTS_KEY, inserted)
        return True


class Py3AlertDest4Es(object):

    @staticmethod
    def cache_inital():
        cache.set_json(NGX_AUD_RESULTS_KEY, [])
        cache.set(NGX_AUD_DELAY_EXP_KEY, 'ANY_VALUE', DELAY_EXP)

    def send(self, msg):
        item = json.loads(str(bytes.decode(msg['LEGACY_MSGHDR'] + msg['MESSAGE'], 'utf-8')))
        if not cache.get(SOURCE_IP_KEY):
            cache.set(SOURCE_IP_KEY, str(msg['SOURCEIP']))
        if not cache.get(HOST_FORM_KEY):
            cache.set(HOST_FORM_KEY, str(msg['HOST_FROM']))
        # 存储告警记录的 cache_key
        inserted = cache.get_json(NGX_AUD_RESULTS_KEY)
        if not inserted:
            cache.set_json(NGX_AUD_RESULTS_KEY, [])
            inserted = []
        expired = cache.get(NGX_AUD_DELAY_EXP_KEY)
        count_inserted = len(inserted)
        if count_inserted > NGX_AUD_MAX_INSERT_NUM or not expired:
            if count_inserted < 1:
                logging.info('[Alert]响应时间到；准备插入单条')
                inserted.append(item)
            docs = []
            for x in inserted:
                _item = parse_nginx_alert_item(x)
                _tmp = NginxAlertLog(meta={'id': _item["unique_id"]}, **_item)
                docs.append(_tmp)
            bulk(client=client, actions=[{
                "_index": NginxAlertLog._index._name,
                "_type": "_doc",
                "_source": x
            } for x in docs])
            logging.info('[Alert]批量插入【{}】条nginx_alert记录到Es数据库!'.format(str(len(docs))))
            Py3AlertDest4Es.cache_inital()

        else:
            logging.info('[Alert]记录到Redis数据库准备多条插入! 【 {cur} / {max}】'.format(cur=len(inserted), max=NGX_AUD_MAX_INSERT_NUM))
            inserted.append(item)
            cache.set_json(NGX_AUD_RESULTS_KEY, inserted)
        return True


class Py3ErrorDest4Es(object):

    @staticmethod
    def cache_inital():
        cache.set_json(NGX_ERR_RESULTS_KEY, [])
        cache.set(NGX_ERR_DELAY_EXP_KEY, 'ANY_VALUE', DELAY_EXP)

    def send(self, msg):

        item_str = str(bytes.decode(msg['LEGACY_MSGHDR'] + msg['MESSAGE'], 'utf-8'))
        item = parse_nginx_error_mod_log(item_str)

        # 存储告警记录的 cache_key
        inserted = cache.get_json(NGX_ERR_RESULTS_KEY)
        if not inserted:
            cache.set_json(NGX_ERR_RESULTS_KEY, [])
            inserted = []
        expired = cache.get(NGX_ERR_DELAY_EXP_KEY)
        count_inserted = len(inserted)
        if count_inserted > NGX_ERR_MAX_INSERT_NUM or not expired:
            if count_inserted < 1:
                logging.info('[Ng_Error]响应时间到；准备插入单条')
                inserted.append(item)
            docs = []
            for x in inserted:
                _tmp = NginxAlertLog(meta={'id': x["unique_id"]}, **x)
                docs.append(_tmp)
            bulk(client=client, actions=[{
                "_index": NginxErrorLog._index._name,
                "_type": "_doc",
                "_source": x
            } for x in docs])
            logging.info('[Ng_Error]批量插入【{}】条nginx_error记录到Es数据库!'.format(str(len(docs))))
            Py3ErrorDest4Es.cache_inital()

        else:
            logging.info(
                '[Ng_Error]记录到Redis数据库准备多条插入! 【 {cur} / {max}】'.format(cur=len(inserted), max=NGX_ERR_MAX_INSERT_NUM))
            inserted.append(item)
            cache.set_json(NGX_ERR_RESULTS_KEY, inserted)
        return True


NginxErrorLog.init()
