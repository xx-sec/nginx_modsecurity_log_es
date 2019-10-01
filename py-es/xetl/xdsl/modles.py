from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections, Ip, Float

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
    request = Text(analyzer='snowball')
    http_x_forwarded_for = Text(analyzer='snowball')
    http_referer = Text(analyzer='snowball')
    time_local = Date() 
    request_time = Float() 
    upstream_response_time = Float() 
    upstream_status = Text(analyzer='snowball')
    upstream_addr = Text(analyzer='snowball')
    http_user_agent = Text(analyzer='snowball')

    class Index:
        name = 'nginx_access_log'
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



