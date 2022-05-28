from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import List

import backoff
from psycopg2 import connect as pgconnect
from psycopg2 import sql
from psycopg2.extras import DictCursor

from etl.sql_templates import (FILM_BY_ID, GENRE_BY_ID, PERSON_BY_ID,
                               STARTED_TIME, UPDATE_IDS)
from models import films, genres, persons
from models.supporting_class import ModifiedIs


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

    def get_started_time(self, table: str) -> datetime:
        sqlquery = sql.SQL(STARTED_TIME).format(table=sql.Identifier(table))
        modified_time = self.pg_query(
            sqlquery=sqlquery,
            queryargs=None,
            single=True,
        )
        return modified_time[0] - timedelta(seconds=1)

    def get_update_object(
        self, table: str, lasttime: datetime, limit: int = None,
    ) -> list[ModifiedIs]:
        sqlquery = sql.SQL(UPDATE_IDS).format(table=sql.Identifier(table))
        rows = self.pg_query(
            sqlquery=sqlquery,
            queryargs=(lasttime, limit),
            single=False,
        )
        return [ModifiedIs(**row).id for row in rows]

    def get_genre_by_id(self, ids: List[str]) -> List[genres.Genre]:
        rows = self.pg_query(
            sqlquery=GENRE_BY_ID,
            queryargs=(ids,),
            single=False,
        )
        return [genres.Genre(**row) for row in rows]

    def get_person_by_id(self, ids: List[str]) -> List[persons.PersonForFolm]:
        rows = self.pg_query(
            sqlquery=PERSON_BY_ID,
            queryargs=(ids,),
            single=False,
        )
        return [persons.PersonDetails(**row) for row in rows]

    def get_film_by_id(self, ids: List[str]) -> List[films.Film]:
        rows = self.pg_query(
            sqlquery=FILM_BY_ID,
            queryargs=(ids,),
            single=False,
        )
        return [
            films.Film(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                rating=row['rating'],
                type=row['type'],
                genres_names=row['genres_names'],
                actors_names=row['actors_names'],
                directors_names=row['directors_names'],
                writers_names=row['writers_names'],
                genres=[
                    genres.Genre(**self._genre_split(genre))
                    for genre in row['genres']
                ] if row['genres'] is not None else [],
                actors=[
                    persons.PersonForFolm(**self._person_split(actor))
                    for actor in row['actors']
                ] if row['actors'] is not None else [],
                directors=[
                    persons.PersonForFolm(**self._person_split(director))
                    for director in row['directors']
                ] if row['directors'] is not None else [],
                writers=[
                    persons.PersonForFolm(**self._person_split(writer))
                    for writer in row['writers']
                ] if row['writers'] is not None else [],
            )
            for row in rows
        ]

    def _genre_split(self, row):
        if row is None:
            return None
        genre = row.split(' : ')
        return {
            'id': genre[0],
            'name': genre[1],
            'description': genre[2],
        }

    def _person_split(self, row):
        if row is None:
            return None
        person = row.split(' : ')
        return {
            'id': person[0],
            'name': person[1],
        }

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
