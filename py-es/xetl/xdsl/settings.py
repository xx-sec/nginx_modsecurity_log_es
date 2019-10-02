# coding:utf-8

ES_HOSTS =['http://elastic:test@1q2w2e4R@localhost:9200', ]

# SOURCE_IP HOST_FORM
SOURCE_IP_KEY = 'source_ip'
HOST_FORM_KEY = 'host_from'

# REDIS_CFG = "redis://sqsjywl123@localhost:6379"
REDIS_HOST = '192.168.1.5'
REDIS_PORT = 6379
REDIS_PASSWORD = 'sqsjywl123'
REDIS_DB = 10

OPS_LOG_FILE = '/spool/log/sloges.log'

# 访问日志的初始化
NGX_REDIS_RESULTS_KEY = "ngx_access_results"
NGX_MAX_INSERT_NUM = 200
DELAY_EXP_KEY1 = 'expire_Key1'
DELAY_EXP = 10  # 延迟10s 如果结果有了就一次插入。
DELAY_RECODE_KEY1 = 'ngx_access_log_delay_key'  # 设置改键盘存活。

# 告警日志的管理
DELAY_RECODE_KEY2 = 'ngx_alert_log_delay_key'  # 设置改键盘存活。
NGX_MAX_INSERT_NUM2 = 10


