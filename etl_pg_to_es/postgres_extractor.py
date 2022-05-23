import backoff
import psycopg2
from psycopg2 import connect as pgconnect, sql
from psycopg2.extras import DictCursor


class PostgresExtractor(object):
    def __init__(self, postgres_dsl):
        self.cnf = postgres_dsl
        self.conn = self._connect()

    @backoff.on_exception(backoff.expo, psycopg2.Error, max_time=60)
    def pg_single_query(self, sqlquery: str, queryargs: tuple) -> list:
        self.conn = self._connect() if self.conn.closed != 0 else self.conn
        with self.conn as conn, conn.cursor as cursor:
            cursor.execute(sqlquery, queryargs)
            row = cursor.fetchone()
        return row

    @backoff.on_predicate(backoff.fibo, max_time=60)
    def _connect(self):
        return pgconnect(
            dbname=self.cnf.postgres_db,
            user=self.cnf.postgres_user,
            password=self.cnf.postgres_password,
            host=self.cnf.postgres_host,
            port=self.cnf.postgres_port,
            options='-c search_path={schema}'.format(
                schema=self.cnf.postgres_schema,
            ),
        )


if __name__ == '__main__':
    from config import Settings
    extractor = PostgresExtractor(Settings())
    sqlquery = sql.SQL(
        'SELECT modified FROM {table} ORDER BY modified LIMIT 1',
    ).format(
        table=sql.Identifier('genre'),
    )
    query = extractor.pg_single_query(sqlquery, None)
    print(query)
