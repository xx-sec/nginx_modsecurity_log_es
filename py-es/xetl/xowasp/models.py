from elasticsearch_dsl import Document, Date, Integer, Text, connections, Ip, Float, Object, Keyword, Boolean

from xdsl.settings import ES_HOSTS

# Define a default Elasticsearch client
client = connections.create_connection(hosts=ES_HOSTS)


class ModsecRule(Document):
    rule_id = Integer()
    msg = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    rule_txt = Text(analyzer='snowball')
    severity = Text(analyzer='snowball')
    phase = Text(analyzer='snowball')
    rev = Text(analyzer='snowball')
    maturity = Text(analyzer='snowball')
    accuracy = Text(analyzer='snowball')
    ver = Text(analyzer='snowball')
    filename = Text(analyzer='snowball')

    class Index:
        name = 'modsec_rules'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        return super(ModsecRule, self).save(**kwargs)


ModsecRule.init()