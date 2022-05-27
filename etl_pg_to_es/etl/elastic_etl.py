import backoff
from elasticsearch import Elasticsearch, exceptions, helpers
from pydantic.main import BaseModel


class ElasticETL(object):
    def __init__(self, elastic_dns):
        self.dns = elastic_dns
        self.es = self.connect()

    def connect(self):
        return Elasticsearch(
            hosts=self.dns.elastic_host,
            port=self.dns.elastic_port,
            scheme=self.dns.elastic_scheme,
            http_auth=(self.dns.elastic_user, self.dns.elastic_password),
        )

    def create_index(self, index='', body=''):
        if not self.es.indices.exists(index=index):
            self.es.indices.create(index=index, body=body)

    @backoff.on_predicate(backoff.expo, max_time=60)
    def set_bulk(self, index, data):
        try:
            return helpers.bulk(
                self.es, self.generate_elastic_data(index, data),
            )
        except exceptions.ConnectionError:
            self.connect()
            return helpers.bulk(
                self.es, self.generate_elastic_data(index, data),
            )

    def generate_elastic_data(self, index, data: list[BaseModel]):
        yield from (
            {
                '_index': index,
                '_id': item.id,
                '_source': item.json(),
            }
            for item in data
        )
