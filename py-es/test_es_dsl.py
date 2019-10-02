from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections, Object

# Define a default Elasticsearch client
client = connections.create_connection(hosts=['http://elastic:test@1q2w2e4R@192.168.1.5:9200/', ])
### https://github.com/elastic/elasticsearch-dsl-py

class Article(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()
    to = Object

    class Index:
        name = 'blog3'
        settings = {
          "number_of_shards": 2,
        }

    @classmethod
    def tojson(cls):
        return dict(
            # title=cls.title,
            # body=cls.body,
            tags=cls.tags,
            published_from=cls.published_from,
            lines=cls.lines,
            to=cls.to,
        )

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(** kwargs)

    def is_published(self):
        return datetime.now() > self.published_from


# create the mappings in elasticsearch
Article.init()


# create and save and article
def add_article(id, tag, ):
    article = Article(meta={'id': id}, title='Hello world Test233!', tags=['test', tag], to={"name": 2323})
    article.body = ''' bbcackkcdalooong text '''
    return article


datas = []
for x in [x+20 for x in range(10055)]:
    _d = add_article(x, 'ops')
    datas.append(_d)

from elasticsearch.helpers import bulk

actions = [{
    "_index": 'blog3',
    "_type": "_doc",
    "_source": x
    } for x in datas]


# bulk(client=client, actions=actions)
print(Article._index._name)

for x in Article.search():
    print("||||||||||||||||||||||||||||||||")
    print(x.to_dict())
    print(x)
    print("===================")

# Display cluster health
print(connections.get_connection().cluster.health())