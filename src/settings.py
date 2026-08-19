from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    token: str = Field(alias="TELEGRAM_BOT_TOKEN")


class SpbstuSettings(BaseSettings):
    program_candidates_list_url: str = Field(
        alias="SPBSTU_PROGRAM_CANDIDATES_LIST_URL",
        default="https://my.spbstu.ru/home/get-abit-list"
    )
    codes_list_url: str = Field(
        alias="SPBSTU_CODES_LIST_URL",
        default="https://my.spbstu.ru/home/get-code-list"
    )


@dataclass
class Settings:
    bot_settings: BotSettings
    spbstu_settings: SpbstuSettings


@lru_cache
def get_settings() -> Settings:
    load_dotenv()

    return Settings(
        bot_settings=BotSettings(),
        spbstu_settings=SpbstuSettings(),
    )
