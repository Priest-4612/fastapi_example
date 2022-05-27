import pprint

from core.config import ElasticDns, PostgresDsn
from etl.elastic_etl import ElasticETL
from etl.postgres_etl import PostgresExtractor
from es_index import ELASTIC_INDEX


def init_elastic(es: ElasticETL, indexes: dict) -> None:
    for index, body in indexes.items():
        es.create_index(index=index, body=body)


if __name__ == '__main__':
    extractor = PostgresExtractor(PostgresDsn())
    es = ElasticETL(ElasticDns())
    init_elastic(es, ELASTIC_INDEX)
    lasttime = extractor.get_started_time('person')
    update_list = extractor.get_update_object('person', lasttime, limit=1)
    film_list = extractor.get_person_by_id(tuple(update_list))
    [pprint.pprint(film) for film in film_list]

    # pprint.pprint(ELASTIC_INDEX['GENRE_INDEX']['body'])
