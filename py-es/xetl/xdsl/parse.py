import json 

from xdsl.utils import get_pydt_based_logdt

def parse_nginx_log_item(msg):
    item = json.loads(str(bytes.decode(msg['LEGACY_MSGHDR'] + msg['MESSAGE'], 'utf-8')))
    log_host = str(msg['HOST_FROM'])
    log_source = str(msg['SOURCEIP'])

    if item["upstream_response_time"] == '-':
        item["upstream_response_time"] = '0.00'

    if item["request_time"] == '-':
        item["request_time"] = '0.00'

    # 时间
    item['time_local'] = get_pydt_based_logdt(item['time_local'])

    return dict(
        log_host=log_host,
        log_source=log_source,
        **item
    )