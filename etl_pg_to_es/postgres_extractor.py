from contextlib import contextmanager

import backoff
from psycopg2 import connect as pgconnect
from psycopg2 import sql
from psycopg2.extras import DictCursor


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
    sqlquery = sql.SQL(
        'SELECT * FROM {table} ORDER BY modified Limit 1',
    ).format(
        table=sql.Identifier('person'),
    )
    query = extractor.pg_query(sqlquery=sqlquery, queryargs=None, single=False)
    pprint.pprint(query)
