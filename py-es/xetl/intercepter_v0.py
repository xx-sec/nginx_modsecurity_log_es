import redis 
import json 

# from xdsl.test import test_insert_example
from xdsl.parse import parse_nginx_log_item
from xdsl.modles import NginxAccessLog, client


class Py3Destination4Es(object):
    def send(self, msg):
        item = parse_nginx_log_item(msg)
        _tmp = NginxAccessLog(meta={'id': item["request_id"] }, **item)
        _tmp.save(using=client) 
        return True
