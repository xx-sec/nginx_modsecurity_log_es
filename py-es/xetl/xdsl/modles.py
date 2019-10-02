from elasticsearch_dsl import Document, Date, Integer, Text, connections, Ip, Float, Object, Keyword

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
    upstream_response_time = Float() 
    upstream_status = Text(analyzer='snowball')
    upstream_addr = Text(analyzer='snowball')
    http_user_agent = Text(analyzer='snowball')

    # 2019-9-22 增加了 OS
    os = Text(analyzer='snowball')
    device = Text(analyzer='snowball')
    user_agent = Text(analyzer='snowball')

    class Index:
        name = 'ngx_access_log'
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
    """
    {"transaction":{"client_ip":"127.0.0.1",
    "time_stamp":"Wed Oct  2 08:07:01 2019",
    "server_id":"e74dde9f8eb44d5b0093491a543ac04a9f54d99c",
    "client_port":38764,"host_ip":"127.0.0.1",
    "host_port":2380,
    "unique_id":"15700180210.267978",
    "request":{"method":"GET",
    "http_version":1.0,"uri":"/",
    "headers":{"Host":"localhost:2380","User-Agent":"ApacheBench/2.3","Accept":"*/*"}},
    "response":{"http_code":403,"headers":{"Server":"nginx","Date":"Wed, 02 Oct 2019 12:07:01 GMT","Content-Length":"554","Content-Type":"text/html","Connection":"close"}},"producer":{"modsecurity":"ModSecurity v3.0.3 (Linux)","connector":"ModSecurity-nginx v1.0.0","secrules_engine":"Enabled","components":["OWASP_CRS/3.1.0\""]},"messages":[]}}
    """
    insert_date = Date()
    log_host = Text(analyzer='snowball')
    log_source = Text(analyzer='snowball')  # 可以设置为IP

    request = Object()


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



