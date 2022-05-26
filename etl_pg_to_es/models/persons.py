from typing import List, Optional

from pydantic import BaseConfig, Field

from models.mixin_orjson import OrjsonMixin


class PersonForFolm(OrjsonMixin):
    id: str = Field(..., alias='uuid')
    name: str = Field(..., alias='full_name')

    class Config(BaseConfig):
        allow_population_by_field_name = True


class PersonDetails(OrjsonMixin):
    id: str = Field(..., alias='uuid')
    name: str = Field(..., alias='full_name')
    role: List[Optional[str]]
    film_ids: List[Optional[str]] = Field(..., alias='film_ids')
    actor_film_ids: Optional[List[str]] = Field(..., alias='actor')
    director_film_ids: Optional[List[str]] = Field(..., alias='director')
    writer_film_ids: Optional[List[str]] = Field(..., alias='writer')

    class Config(BaseConfig):
        allow_population_by_field_name = True
