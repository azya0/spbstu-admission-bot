from functools import lru_cache
from typing import Callable

from redis import Redis

from .settings import get_redis_settings, RedisSettings


USER_TO_CHAT_DB_INDEX = 0


@lru_cache
def _get_redis_db(redis_settings: RedisSettings = get_redis_settings()) -> Callable[[int], Redis]:
    return lambda db_index: Redis(
        host=redis_settings.host,
        port=redis_settings.port,
        db=db_index
    )


def get_user_to_chat_db(connection_info: Callable[[int], Redis] = _get_redis_db()) -> Redis:
    return connection_info(USER_TO_CHAT_DB_INDEX)
