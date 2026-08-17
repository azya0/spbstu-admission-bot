from typing import Sequence

from redis import Redis

from database import DictDatabase
from database.exception import DictDatabaseKeyNotFound

from .client import get_user_to_chat_db


class RedisDatabase(DictDatabase):
    def __init__(self, connection: Redis):
        self.connection = connection

    def set(self, key: str, value: str) -> None:
        self.connection.set(key, value)

    def get(self, key: str) -> str:
        data = self.connection.get(key)

        if data is None:
            raise DictDatabaseKeyNotFound(key)

        return data.decode()

    def get_keys(self) -> Sequence[str]:
        return [key.decode() for key in self.connection.scan_iter()]


def get_user_db(connection: Redis = get_user_to_chat_db()) -> RedisDatabase:
    return RedisDatabase(connection)
