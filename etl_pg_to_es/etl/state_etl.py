import abc
from typing import Any

import backoff
from aioredis import Redis


class BaseStorage(object):
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища."""


class State(object):
    """
    Класс для хранения состояния при работе с данными.

    Чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или
    распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, state: Any) -> None:
        """Установить состояние для определённого ключа."""
        self.storage.save_state({key: state})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        state = self.storage.retrieve_state()
        if key not in state.keys():
            return None
        state_object = state[key]
        if isinstance(state_object, 'bytes'):
            return state_object.decode('utf8')
        return state_object


class RedisStorage(BaseStorage):
    def __init__(self, redis_dsl: [dict, None] = None):
        self.redis_dsl = redis_dsl
        self.redis_conn = None

    @backoff.on_predicate(backoff.expo, max_time=60)
    def connect(self) -> None:
        self.redis_conn = Redis(
            host=self.redis_dsl.redis_host,
            port=self.redis_dsl.redis_port,
            password=self.redis_dsl.redis_password,
            decode_responses=True,
        )

    @backoff.on_predicate(backoff.expo, max_time=60)
    def retrieve_state(self) -> dict:
        if not self.redis_conn.ping():
            self.connect()
        return self.redis_conn

    @backoff.on_predicate(backoff.expo, max_time=60)
    def save_state(self, state: dict) -> None:
        if not self.redis_conn.ping():
            self.connect()
        self.redis_conn.mset(state)

    def __del__(self):
        if self.redis_conn:
            self.redis_conn.close()
