from core.config import ElasticDns, PostgresDsn
from es_index import ELASTIC_INDEX
from etl.elastic_etl import ElasticETL
from etl.postgres_etl import PostgresExtractor


def init_elastic(es: ElasticETL, indexes: dict) -> None:
    for index, body in indexes.items():
        es.create_index(index=index, body=body)


if __name__ == '__main__':
    extractor = PostgresExtractor(PostgresDsn())
    es = ElasticETL(ElasticDns())
    init_elastic(es, ELASTIC_INDEX)
    lasttime = extractor.get_started_time('film_work')
    update_list = extractor.get_update_object('film_work', lasttime, limit=1)
    film_list = extractor.get_film_by_id(tuple(update_list))
    print(es.set_bulk('movies', film_list))
