import orjson
from pydantic import BaseConfig, BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
    id: str
    title: str
    description: str

    class Config(BaseConfig):
        json_loads = orjson.loads
        json_dumps = orjson_dumps
