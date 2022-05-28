import time
from datetime import datetime

from core.config import ElasticDsn, PostgresDsn, RedisDsn, Settings
from es_index import ELASTIC_INDEX
from etl.elastic_etl import ElasticETL
from etl.postgres_etl import PostgresExtractor
from etl.state_etl import RedisStorage, State


def init_elastic(es: ElasticETL, indexes: dict) -> None:
    for index, body in indexes.items():
        es.create_index(index=index, body=body)


def update_elastic_data(es: ElasticETL, pg: PostgresExtractor, lasttime=None):
    es.set_bulk(
        index='genres',
        body=pg.get_genre_by_id(
            lasttime=lasttime,
        ),
    )
    es.set_bulk(
        index='persons',
        body=pg.get_person_by_id(
            lasttime=lasttime,
        ),
    )
    es.set_bulk(
        index='movies',
        body=pg.get_film_by_id(
            lasttime=lasttime,
        ),
    )


def run(state: State, pg: PostgresExtractor, es: ElasticETL):
    start_time = state.get_state('start_time')
    if start_time is None:
        start_time = datetime(2000, 1, 1)
    update_elastic_data(es, pg, start_time)


if __name__ == '__main__':
    redis_storage = RedisStorage(RedisDsn())
    state = State(redis_storage)
    pg = PostgresExtractor(PostgresDsn())
    es = ElasticETL(ElasticDsn())
    init_elastic(es, ELASTIC_INDEX)

    while True:
        run(state, pg, es)
        time.sleep(Settings().timeout)
