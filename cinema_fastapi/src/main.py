import logging
from pathlib import Path

import aioredis
import uvicorn
from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films
from core.config import Settings
from core.logger import LOGGING
from db import elastic, redis

ENV_PATH = Path(__file__).resolve().parents[2].joinpath('env', '.env')
load_dotenv(dotenv_path=ENV_PATH)

config = Settings()

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis_dsl = (config.REDIS_HOST, config.REDIS_PORT)
    redis_pool_min = 10
    redis_pool_max = 20
    redis.redis = await aioredis.create_redis_pool(
        redis_dsl,
        minsize=redis_pool_min,
        maxsize=redis_pool_max,
    )
    elastic.es = AsyncElasticsearch(
        hosts=['{host}:{port}'.format(
            host=config.ELASTIC_HOST,
            port=config.ELASTIC_PORT,
        )],
    )


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
