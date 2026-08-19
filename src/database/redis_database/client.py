from collections.abc import Callable
from functools import lru_cache

from redis import Redis

from .settings import RedisSettings, get_redis_settings

CHAT_TO_SPBSTU_USER_DB_INDEX = 0


@lru_cache
def _get_redis_db(redis_settings: RedisSettings = get_redis_settings()) -> Callable[[int], Redis]:
    return lambda db_index: Redis(
        host=redis_settings.host,
        port=redis_settings.port,
        db=db_index
    )

def get_chat_to_spbstu_user_db(connection_info: Callable[[int], Redis] = _get_redis_db()) -> Redis:
    return connection_info(CHAT_TO_SPBSTU_USER_DB_INDEX)
