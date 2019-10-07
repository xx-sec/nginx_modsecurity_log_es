from elasticsearch_dsl import Document, Date, Integer, Text, connections, Ip, Float, Object, Keyword, Boolean

from xdsl.settings import ES_HOSTS

# Define a default Elasticsearch client
client = connections.create_connection(hosts=ES_HOSTS)


class NginxAccessLog(Document):
    insert_date = Date()
    log_host = Text(analyzer='snowball')
    log_source = Text(analyzer='snowball') # 可以设置为IP
    request_id = Text(analyzer='snowball')
    host = Text(analyzer='snowball')
    domain = Text(analyzer='snowball')
    remote_user = Text(analyzer='snowball')
    remote_addr = Ip()
    server_addr = Ip()
    server_port = Integer()
    request = Text(analyzer='snowball')
    method = Text(analyzer='snowball')
    url = Text(analyzer='snowball')
    args = Text(analyzer='snowball')
    status = Integer()
    http_x_forwarded_for = Text(analyzer='snowball')
    http_referer = Text(analyzer='snowball')
    time_local = Date() 
    request_time = Float()
    # 这个原本使用的是 float 后来发现是两个值
    upstream_response_time = Text(analyzer='snowball')
    upstream_status = Text(analyzer='snowball')
    upstream_addr = Text(analyzer='snowball')
    http_user_agent = Text(analyzer='snowball')

    # 2019-9-22 增加了 OS
    os = Text(analyzer='snowball')
    device = Text(analyzer='snowball')
    user_agent = Text(analyzer='snowball')

    class Index:
        name = 'ngx_access_log_v1'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        if not self.log_host:
            self.log_host = '127.0.0.1'
        if not self.log_source:
            self.log_source = '127.0.0.1'
        
        return super(NginxAccessLog, self).save(** kwargs)


NginxAccessLog.init()


class NginxAlertLog(Document):

    insert_date = Date()
    log_host = Text(analyzer='snowball')
    log_source = Text(analyzer='snowball')  # 可以设置为IP

    time_stamp = Date()
    server_id = Text(analyzer='snowball')
    client_port = Integer()
    host_ip = Ip()
    host_port = Integer()
    unique_id = Text(analyzer='snowball')
    request = Object()
    response = Object()
    producer = Object()
    messages = Object()
    missing = Boolean()

    msg = Text(analyzer='snowball')
    rule_id = Integer()

    class Index:
        name = 'nginx_alert_log'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        if not self.log_host:
            self.log_host = '127.0.0.1'
        if not self.log_source:
            self.log_source = '127.0.0.1'
        return super(NginxAlertLog, self).save(**kwargs)


NginxAlertLog.init()


# todo missing 的消息进行补充; json日志存在丢失情况下的补充。
class NginxErrorLog(Document):

    insert_date = Date()

    unique_id = Text(analyzer='snowball')
    messages = Object()
    body = Text(analyzer='snowball')

    class Index:
        name = 'nginx_error_log'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        if not self.log_host:
            self.log_host = '127.0.0.1'
        if not self.log_source:
            self.log_source = '127.0.0.1'

        return super(NginxErrorLog, self).save(**kwargs)


NginxErrorLog.init()


