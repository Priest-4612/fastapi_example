from logging import config as logging_config
from pathlib import Path

from pydantic import BaseConfig, BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_HOST: str
    PROJECT_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    BASE_DIR: Path = Path(__file__).resolve().parent

    class Config(BaseConfig):
        fields = {
            'PROJECT_NAME': {'env': 'PROJECT_NAME'},
            'PROJECT_HOST': {'env': 'PROJECT_HOST'},
            'PROJECT_PORT': {'env': 'PROJECT_PORT'},
            'REDIS_HOST': {'env': 'REDIS_HOST'},
            'REDIS_PORT': {'env': 'REDIS_PORT'},
            'ELASTIC_HOST': {'env': 'ELASTIC_HOST'},
            'ELASTIC_PORT': {'env': 'ELASTIC_PORT'},
        }
