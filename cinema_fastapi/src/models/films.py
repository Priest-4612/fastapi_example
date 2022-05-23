import orjson
from pydantic import BaseConfig, BaseModel


def orjson_dumps(val, *, default):
    return orjson.dumps(val, default=default).decode()


class Film(BaseModel):
    id: str
    title: str
    description: str

    class Config(BaseConfig):
        json_loads = orjson.loads
        json_dumps = orjson_dumps
