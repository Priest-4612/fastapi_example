import pprint

from etl.postgres_etl import PostgresExtractor
from core.config import PostgresDsn

if __name__ == '__main__':
    extractor = PostgresExtractor(PostgresDsn())
    lasttime = extractor.get_start_modified_time_object('genre')
    update_list = extractor.get_update_object('genre', lasttime, limit=5)
    film_list = extractor.get_genre_by_id(tuple(update_list))
    [pprint.pprint(film.json()) for film in film_list]
