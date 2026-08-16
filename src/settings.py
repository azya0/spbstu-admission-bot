from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


load_dotenv()


class BotSettings(BaseSettings):
    token: str = Field(alias="TELEGRAM_BOT_TOKEN")


class SpbstuSettings(BaseSettings):
    id: int = Field(alias="SPBSPU_ID")
    url: str = Field(alias="SPBSPU_URL")


@dataclass
class Settings:
    bot_settings: BotSettings
    spbstu_settings: SpbstuSettings


@lru_cache
def get_settings() -> Settings:
    return Settings(
        bot_settings=BotSettings(),
        spbstu_settings=SpbstuSettings(),
    )
