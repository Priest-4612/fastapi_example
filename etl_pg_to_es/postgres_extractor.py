from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import List

import backoff
from psycopg2 import connect as pgconnect
from psycopg2 import sql
from psycopg2.extras import DictCursor

from models.supporting_class import ModifiedIs
from models import films, genres, persons


class PostgresExtractor(object):
    def __init__(self, postgres_dsn):
        self.dsn = postgres_dsn
        self.conn = self._connect()

    @backoff.on_predicate(backoff.expo, max_time=60)
    def pg_query(self, sqlquery: str, queryargs: tuple, single: bool) -> list:
        if self.conn.closed != 0:
            self.conn = self._connect()
        with self._postgres_cursor() as cursor:
            rows = None
            cursor.execute(sqlquery, queryargs)
            rows = cursor.fetchone() if single else cursor.fetchall()
        return rows

    def get_start_modified_time_object(self, table: str) -> datetime:
        sql_tmp = """
            SELECT modified
            FROM {table}
            ORDER BY modified
        """
        sqlquery = sql.SQL(sql_tmp).format(table=sql.Identifier(table))
        modified_time = self.pg_query(
            sqlquery=sqlquery,
            queryargs=None,
            single=True,
        )
        return modified_time[0] - timedelta(seconds=1)

    def get_update_object(
        self, table: str, lasttime: datetime, limit: int,
    ) -> list[ModifiedIs]:
        sql_tmp = """
            SELECT id, created, modified
            FROM {table}
            WHERE modified > %s
            ORDER BY modified
            LIMIT %s
        """
        sqlquery = sql.SQL(sql_tmp).format(table=sql.Identifier(table))
        rows = self.pg_query(
            sqlquery=sqlquery,
            queryargs=(lasttime, limit),
            single=False,
        )
        return [ModifiedIs(**row).id for row in rows]

    def get_genre_by_id(self, ids: List[str]) -> List[genres.Genre]:
        sql_tmp = """
            SELECT *
            FROM genre
            WHERE id IN %s
        """
        rows = self.pg_query(sqlquery=sql_tmp, queryargs=(ids,), single=False)
        return [genres.Genre(**row) for row in rows]

    def get_film_by_id(self, ids: List[str]) -> List[films.Film]:
        sql_tmp = """
            SELECT
            fw.id, fw.title, fw.description, fw.rating, fw.type,
            ARRAY_AGG(DISTINCT g.name) AS genres,
            ARRAY_AGG(DISTINCT p.id || ' : ' || p.full_name)
            FILTER (WHERE pfw.role = 'director') AS directors,
            ARRAY_AGG(DISTINCT p.id || ' : ' || p.full_name)
            FILTER (WHERE pfw.role = 'actor') AS actors,
            ARRAY_AGG(DISTINCT p.id || ' : ' || p.full_name)
            FILTER (WHERE pfw.role = 'writer') AS writers,
            fw.created, fw.modified
            FROM film_work as fw
            LEFT JOIN person_film_work as pfw ON pfw.film_work_id = fw.id
            LEFT JOIN person as p ON p.id = pfw.person_id
            LEFT JOIN genre_film_work as gfw ON gfw.film_work_id = fw.id
            LEFT JOIN genre g ON g.id = gfw.genre_id
            WHERE fw.id IN %s
            GROUP BY fw.id
        """
        rows = self.pg_query(sqlquery=sql_tmp, queryargs=(ids,), single=False)
        return rows
        # return [films.Film(**row) for row in rows]

    @backoff.on_predicate(backoff.expo, max_time=60)
    def _connect(self):
        return pgconnect(
            dbname=self.dsn.postgres_db,
            user=self.dsn.postgres_user,
            password=self.dsn.postgres_password,
            host=self.dsn.postgres_host,
            port=self.dsn.postgres_port,
            options='-c search_path={schema}'.format(
                schema=self.dsn.postgres_schema,
            ),
            cursor_factory=DictCursor,
        )

    @contextmanager
    def _postgres_cursor(self):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            conn.close()


if __name__ == '__main__':
    import pprint

    from core.config import PostgresDsn

    extractor = PostgresExtractor(PostgresDsn())
    lasttime = extractor.get_start_modified_time_object('film_work')
    update_list = extractor.get_update_object('film_work', lasttime, limit=1)
    film_list = extractor.get_film_by_id(tuple(update_list))
    pprint.pprint(film_list)
