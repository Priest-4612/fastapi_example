import backoff
import psycopg2
from contextlib import contextmanager
from psycopg2 import connect as pgconnect, sql
from psycopg2.extras import DictCursor


class PostgresExtractor(object):
    def __init__(self, postgres_dsn):
        self.dsn = postgres_dsn
        self.conn = self._connect()

    @backoff.on_exception(backoff.expo, psycopg2.Error, max_time=60)
    def pg_single_query(self, sqlquery: str, queryargs: tuple) -> list:
        if self.conn.closed != 0:
            self.conn = self._connect()
        with self._postgres_connector() as conn:
            cursor = conn.cursor()
            cursor.execute(sqlquery, queryargs)
            row = cursor.fetchone()
        return row

    @backoff.on_predicate(backoff.fibo, max_time=60)
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
        )

    @contextmanager
    def _postgres_connector(self):
        conn = self._connect()
        try:
            yield conn
        finally:
            conn.close()


if __name__ == '__main__':
    from config import PostgresDsn
    extractor = PostgresExtractor(PostgresDsn())
    sqlquery = sql.SQL(
        'SELECT * FROM {table} ORDER BY modified LIMIT 1',
    ).format(
        table=sql.Identifier('genre'),
    )
    query = extractor.pg_single_query(sqlquery, None)
    print(query)
