from functools import lru_cache

from aiogram import Bot as TelegramBot

from settings import Settings, get_settings


@lru_cache
def get_bot(settings: Settings = get_settings()) -> TelegramBot:
    return TelegramBot(token=settings.bot_settings.token)
