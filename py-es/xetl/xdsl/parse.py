import json 
import re

from xdsl.opssdk.utils import get_pydt_based_logdt, get_ua_and_os_from_User_Agent
from xdsl.opssdk.cache import cache
from xdsl.settings import HOST_FORM_KEY, SOURCE_IP_KEY
from xdsl.opssdk.ops_logs import ins_log as logging


def parse_nginx_log_item(item):

    log_host = cache.get(HOST_FORM_KEY)
    log_source = cache.get(SOURCE_IP_KEY)

    # if item["upstream_response_time"] == '-':
    #     item["upstream_response_time"] = '0.00'

    if item["request_time"] == '-':
        item["request_time"] = '0.00'

    # 时间
    item['time_local'] = get_pydt_based_logdt(item['time_local'])
    ua_info = get_ua_and_os_from_User_Agent(item['http_user_agent'])

    return dict(
        log_host=log_host,
        log_source=log_source,
        **item,
        **ua_info
    )


# modsec_audit.log JSON 格式化日志存储和转化
def parse_nginx_alert_item(item):

    log_host = cache.get(HOST_FORM_KEY)
    log_source = cache.get(SOURCE_IP_KEY)
    zd_item = item["transaction"]
    for k, v in item.items():
        if k != "transaction":
            logging.warn('Alert中存在其他有价值的键 【{}】'.format(str(k)))
    zd_item["missing"] = False
    if len(zd_item["messages"]) < 1:
        zd_item["missing"] = True
    # 时间
    zd_item['time_stamp'] = get_pydt_based_logdt(zd_item['time_stamp'])
    return dict(
        log_host=log_host,
        log_source=log_source,
        **zd_item,
    )


# todo 测试之前的 H 阶段日志提取的方法
def get_h_logfile_info(frstr):
    # 首先增加
    _prepare_spk = "YGljdslakfdsF#$#FFHJHHHH==---"
    new_str = frstr.replace("ModSecurity: ", _prepare_spk + "ModSecurity: ")
    res_dict_array = []
    for x in new_str.split(_prepare_spk):
        alert_dct = {}
        if "ModSecurity" in x:
            prefix_partern = re.match("(ModSecurity: .*)\[file.*", x).group(1)
            prefix_len = len(prefix_partern)
            features = re.findall("""\[(\w+)\s"(.*?)"\]""", x[prefix_len:])
            alert_dct['detail'] = prefix_partern
            alert_dct["tags"] = []
            for (key, value) in features:
                if key == "tag":
                    alert_dct["tags"].append(value)
                    continue
                alert_dct[key] = value
            if "message" not in alert_dct.keys():
                try:
                    alert_dct["message"] = alert_dct['detail'].split('. ')[0]
                except :
                    alert_dct["message"] = ""
            if "match" not in alert_dct.keys():
                try:
                    alert_dct["match"] = alert_dct['detail'].split('Matched')[1]
                except Exception as e:
                    logging.error(e)
                    alert_dct["match"] = alert_dct['detail']
            res_dict_array.append(alert_dct)
    return res_dict_array


# 转化 nginx error 里面关于 modsecurity的错误log
def parse_nginx_error_mod_log(item_str):
    messages = get_h_logfile_info(item_str)
    try:
        unique_id = messages[0]["unique_id"]
    except:
        try:
            unique_id = re.match(""".*?\[unique_id "(\d+\.\d+)"\].*?""", item_str).group(1)
        except:
            logging.warn(item_str)
            import uuid
            unique_id = str(uuid.uuid4())

    return dict(
        # log_host=log_host,
        # log_source=log_source,
        unique_id=unique_id,
        messages=messages,
        body=item_str
    )

