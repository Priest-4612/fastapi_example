from typing import List, Optional

from pydantic import BaseConfig, Field

from models import genres, persons
from models.mixin_orjson import OrjsonMixin


class Film(OrjsonMixin):
    id: str = Field(..., alias='uuid')
    title: str
    description: str
    imdb_rating: float = Field(0, alias='rating')
    genres_names: Optional[str]
    actors_names: Optional[str]
    directors_names: Optional[str]
    writers_names: Optional[str]
    genres: Optional[List[genres.Genre]]
    actors: Optional[List[persons.Person]]
    directors: Optional[List[persons.Person]]
    writers: Optional[List[persons.Person]]

    class Config(BaseConfig):
        allow_population_by_field_name = True
