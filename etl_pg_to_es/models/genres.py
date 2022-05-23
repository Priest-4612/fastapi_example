from pydantic import BaseConfig, Field

from models.mixin_orjson import OrjsonMixin, TimeStampedMixin


class Genre(OrjsonMixin, TimeStampedMixin):
    id: str = Field(..., alias='uuid')
    name: str
    description: str

    class Config(BaseConfig):
        allow_population_by_field_name = True
