from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.films import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService(object):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._get_film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _get_film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(
            film.id,
            film.json(),
            expire=FILM_CACHE_EXPIRE_IN_SECONDS,
        )


redis_depends = Depends(get_redis)
elastic_depends = Depends(get_elastic)


@lru_cache()
def get_film_service(
    redis: Redis = redis_depends,
    elastic: AsyncElasticsearch = elastic_depends,
) -> FilmService:
    return FilmService(redis, elastic)
