from asyncio import sleep
from types import CoroutineType
from typing import Any, Callable

from aiogram import Bot as TelegramBot
from aiogram.types import Message

from bot.utils import get_send_message
from database.database import DictDatabase
from database.redis_database import get_user_db
from spbstu.endpoints import get_place_by_user_id
from spbstu.exceptions import UnexpectedStatus

from .bot import get_bot


SLEEP_SECONDS = 30 * 60


async def __periodic_body(user_database: DictDatabase, send_message: Callable[[int, str], CoroutineType[Any, Any, Message]]) -> None:
    for user_id_str in user_database.get_keys():
        chat_id: int = int(user_database.get(user_id_str))

        try:
            user_index = await get_place_by_user_id()
        except UnexpectedStatus as error:
            await send_message(chat_id, f"Ошибка:\n{error}")

        if user_index != -1:
            await send_message(chat_id, f"Ты ещё держишься! {user_index} место!")
            return

        await send_message(chat_id, "Бро... ты больше не в списках...")


async def periodic_message(bot: TelegramBot = get_bot(), user_database: DictDatabase = get_user_db()) -> None:
    send_message = get_send_message(bot)

    while True:
        await __periodic_body(user_database, send_message)

        await sleep(SLEEP_SECONDS)
