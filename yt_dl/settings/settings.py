from functools import lru_cache

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    redis_host: str
    redis_port: int = 6379
    redis_db: int = 0
    redis_pw: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
