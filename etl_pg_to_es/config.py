from pydantic import BaseConfig, BaseSettings


class PostgresDsn(BaseSettings):
    postgres_db: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_schema: str

    class Config(BaseConfig):
        env_file = '../infra/env/.env'


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_password: str
    redis_prefix: str
    elastic_host: str
    elastic_port: int
    elastic_scheme: str
    elastic_user: str
    elastic_password: str
    elastic_index: str
    etl_size_limit: int

    class Config(BaseConfig):
        env_file = '../infra/env/.env'


if __name__ == '__main__':
    cfg = PostgresDsn().dict()
    print(cfg)
