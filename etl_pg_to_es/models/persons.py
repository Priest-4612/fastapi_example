from pydantic import BaseConfig, Field

from models.mixin_orjson import OrjsonMixin


class Person(OrjsonMixin):
    id: str = Field(..., alias='uuid')
    name: str = Field(..., alias='full_name')

    class Config(BaseConfig):
        allow_population_by_field_name = True
