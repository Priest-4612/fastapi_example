import pprint

from etl.postgres_etl import PostgresExtractor
from core.config import PostgresDsn

if __name__ == '__main__':
    extractor = PostgresExtractor(PostgresDsn())
    lasttime = extractor.get_started_time('person')
    update_list = extractor.get_update_object('person', lasttime, limit=1)
    film_list = extractor.get_person_by_id(tuple(update_list))
    [pprint.pprint(film) for film in film_list]
