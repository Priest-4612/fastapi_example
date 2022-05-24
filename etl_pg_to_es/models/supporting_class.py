from pydantic import BaseConfig, Field

from models.mixin_orjson import OrjsonMixin, TimeStampedMixin


class ModifiedIs(OrjsonMixin, TimeStampedMixin):
    id: str = Field(..., alias='uuid')

    class Config(BaseConfig):
        allow_population_by_field_name = True
