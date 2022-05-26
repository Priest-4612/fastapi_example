from typing import Optional

from pydantic import BaseConfig, Field

from models.mixin_orjson import OrjsonMixin


class Genre(OrjsonMixin):
    id: str = Field(..., alias='uuid')
    name: str
    description: Optional[str]

    class Config(BaseConfig):
        allow_population_by_field_name = True
