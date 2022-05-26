from pydantic import BaseConfig, Field

from models.mixin_orjson import OrjsonMixin


class ModifiedIs(OrjsonMixin):
    id: str = Field(..., alias='uuid')

    class Config(BaseConfig):
        allow_population_by_field_name = True
