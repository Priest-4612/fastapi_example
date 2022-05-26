from typing import List, Optional

from pydantic import BaseConfig, Field

from models import genres, persons
from models.mixin_orjson import OrjsonMixin


class Film(OrjsonMixin):
    id: str = Field(..., alias='uuid')
    title: str
    description: str
    imdb_rating: float = Field(0, alias='rating')
    type: str = Field(0, alias='movie')
    genres_names: Optional[List[str]]
    actors_names: Optional[List[str]]
    directors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    genres: Optional[List[genres.Genre]]
    actors: Optional[List[persons.Person]]
    directors: Optional[List[persons.Person]]
    writers: Optional[List[persons.Person]]

    class Config(BaseConfig):
        allow_population_by_field_name = True
