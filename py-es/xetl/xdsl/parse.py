import json 

from xdsl.opssdk.utils import get_pydt_based_logdt, get_ua_and_os_from_User_Agent
from xdsl.opssdk.cache import cache
from xdsl.settings import HOST_FORM_KEY, SOURCE_IP_KEY


def parse_nginx_log_item(item):

    log_host = cache.get(HOST_FORM_KEY)
    log_source = cache.get(SOURCE_IP_KEY)

    if item["upstream_response_time"] == '-':
        item["upstream_response_time"] = '0.00'

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
def parse_nginx_alert_item(msg):
    item = json.loads(str(bytes.decode(msg['LEGACY_MSGHDR'] + msg['MESSAGE'], 'utf-8')))
    log_host = str(msg['HOST_FROM'])
    log_source = str(msg['SOURCEIP'])

    if item["upstream_response_time"] == '-':
        item["upstream_response_time"] = '0.00'

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


# 转化 nginx error 里面关于 modsecurity的错误log
def parse_nginx_error_mod_log(msg):
    pass