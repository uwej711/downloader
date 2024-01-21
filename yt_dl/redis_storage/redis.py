from typing import List

import redis

from ..settings.settings import get_settings
from ..data import Download


DOWNLOADS_KEY = "downloads"


def create_pool() -> redis.ConnectionPool:
    settings = get_settings()

    return redis.ConnectionPool(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_pw,
        decode_responses=True
    )


def get_client() -> redis.Redis:
    return redis.Redis(connection_pool=connection_pool)


connection_pool = create_pool()


def store(download: Download) -> None:
    redis_client = get_client()
    redis_client.set(download.filename, download.model_dump_json())
    redis_client.zadd(DOWNLOADS_KEY, {download.filename: download.created_timestamp})


def get(filename: str) -> Download:
    redis_client = get_client()
    return Download.model_validate_json(redis_client.get(filename))


def list_all() -> List[Download]:
    redis_client = get_client()
    keys = redis_client.zrevrange(DOWNLOADS_KEY, 0, -1)
    return [Download.model_validate_json(redis_client.get(key)) for key in keys]


def delete(filename: str):
    redis_client = get_client()
    redis_client.zrem(DOWNLOADS_KEY, filename)
    redis_client.delete(filename)
