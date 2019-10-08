# coding:utf-8

ES_HOSTS =['http://elastic:test@1q2w2e4R@127.0.0.1:9200', ]

# SOURCE_IP HOST_FORM
SOURCE_IP_KEY = 'source_ip'
HOST_FORM_KEY = 'host_from'

# REDIS_CFG = "redis://sqsjywl123@localhost:6379"
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = 'sqsjywl123'
REDIS_DB = 10

OPS_LOG_FILE = '/spool/log/sloges.log'


DELAY_EXP = 10  # 延迟10s 如果结果有了就一次插入。
# 访问日志的初始化
NGX_ACS_MAX_INSERT_NUM = 200
NGX_ACS_DELAY_EXP_KEY = 'expire_Key1'  # 这个键存活10秒
NGX_ACS_RESULTS_KEY = "ngx_access_results"

# 告警日志的管理
NGX_AUD_MAX_INSERT_NUM = 100
NGX_AUD_DELAY_EXP_KEY = 'expire_Key2'  # 过期设置的key
NGX_AUD_RESULTS_KEY = "ngx_alert_results"

# 错误日志
NGX_ERR_DELAY_EXP_KEY = 'ngx_error_log_delay_key'
NGX_ERR_MAX_INSERT_NUM = 100   # 错误日志最多多条进行插入
NGX_ERR_RESULTS_KEY = "ngx_error_results"  # cache 结果存储的 key
