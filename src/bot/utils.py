from types import CoroutineType
from typing import Any, Callable

from aiogram import Bot
from aiogram.types import Message


def get_send_message(bot: Bot) -> Callable[[int, str], CoroutineType[Any, Any, Message]]:
    return lambda chat_id, message: bot.send_message(chat_id=chat_id, text=message)
