from typing import List, Optional

from pydantic import BaseConfig, Field

from models import genres, persons
from models.mixin_orjson import OrjsonMixin, TimeStampedMixin


class Film(OrjsonMixin, TimeStampedMixin):
    id: str = Field(..., alias='uuid')
    title: str
    description: str
    imdb_rating: float = Field(0, alias='rating')
    genres_names: Optional[str]
    actors_names: Optional[str]
    directors_names: Optional[str]
    writers_names: Optional[str]
    genres: Optional[List[str]]
    actors: Optional[List[str]]
    directors: Optional[List[str]]
    writers: Optional[List[str]]

    class Config(BaseConfig):
        allow_population_by_field_name = True
