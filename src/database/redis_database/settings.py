from functools import lru_cache
from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str = Field(alias="REDIS_HOST", default="localhost")
    port: int = Field(alias="REDIS_PORT", default=6379)


@lru_cache
def get_redis_settings() -> RedisSettings:
    load_dotenv()
    
    return RedisSettings()
