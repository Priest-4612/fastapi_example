import orjson
from pydantic import BaseConfig, BaseModel


def _orjson_dumps(val, *, default):
    return orjson.dumps(val, default=default).decode()


class OrjsonMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = _orjson_dumps
