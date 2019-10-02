from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections

from xdsl.settings import ES_HOSTS

# Define a default Elasticsearch client
client = connections.create_connection(hosts=ES_HOSTS)


class Article(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Index:
        name = 'blog'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(** kwargs)

    def is_published(self):
        return datetime.now() > self.published_from


def test_insert_example():
    print('=======================')


def main():
    # create the mappings in elasticsearch
    Article.init()

    # create and save and article
    article = Article(meta={'id': 42}, title='Hello world!', tags=['test'])
    article.body = ''' looong text '''
    article.published_from = datetime.now()
    article.save()

    article = Article.get(id=42)
    print(article.is_published())

    # Display cluster health
    print(connections.get_connection().cluster.health())


    for x in Article.search():
        print("||||||||||||||||||||||||||||||||")
        print(x)
        print(x.to_dict())
        print("===================")

    datas = []
    for i in [ x +100 for x in range(30)]:
        _t = Article(meta={'id': i }, title='Hello world!', tags=['test'])
        article.body = ''' looong text '''
        article.published_from = datetime.now()
        datas.append(_t)
        print('======burlk ---create')

    from elasticsearch import helpers
    actions = [
        {
            '_op_type': 'index',
            '_index': "blog", 
            '_type': "_doc",
            '_source': d
        }
        for d in datas
    ]    

    helpers.bulk(client, actions)

    for x in Article.search():
        print("||||||||||33333|||||||||||||")
        print(x)
        print(x.to_dict())
        print("===================")


def test2():

    d = '01/Oct/2019:12:11:11 -0400'
    from xdsl.opssdk.utils import get_pydt_based_logdt
    print(get_pydt_based_logdt(d))
    print('========上面是测试时间========')
    from xdsl.modles import NginxAccessLog
    for x in NginxAccessLog.search():
        print("|||||22|||||22222||||222|||||||||")
        print(x)
        print(x.to_dict())
        print("===================")


def test3():
    from xdsl.modles import NginxAccessLog
    # NginxAccessLog.init()
    data = {"request_id":"f75edddda3e4ba07032fa2cef903a41b","server_addr":"127.0.0.1","host":"localhost","domain":"waf_default","server_port":"2380","remote_addr":"127.0.0.1","remote_user":"-","body_bytes_sent":554,"time_local":"01/Oct/2019:12:26:01 -0400","request":"GET / HTTP/1.0","request_method":"GET","url":"/","args":"-","status":"403","http_referer":"-","http_x_forwarded_for":"-","request_time":0.000,"upstream_response_time":"-","upstream_addr":"-","upstream_status":"-","http_user_agent":"ApacheBench/2.3" }
    c = data.copy()
    for k,v in c.items():
        if v == '-':
            data[k] = '0.00'
    data['time_local'] = datetime.now()
    _t = NginxAccessLog(meta={"id": 11}, **data)
    _t.save() 

    for x in NginxAccessLog.search():
        print(x.to_dict())
    

def test_redis():
    from xdsl.opssdk.cache import Cache
    cache = Cache(host='192.168.1.5', password='sqsjywl123', decode_responses=False)
    # cache.set('a', '232323', 111)

    if not cache.get_json('b', {}):
        cache.set_json('b', [1232123, 12312])
    print(type(cache.get_json('b')))

    ## private 会加密和解密失败; 所以不要用 private
    #
    cache.delete('*')
    cache.clear()


