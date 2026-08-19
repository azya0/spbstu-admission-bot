from asyncio import sleep
from collections.abc import Callable
from types import CoroutineType
from typing import Any

from aiogram import Bot as TelegramBot
from aiogram.types import Message

from bot.utils import get_send_message
from database.database import DictDatabase
from database.redis_database import get_user_spbstu_db
from spbstu.endpoints import get_place_by_user_id
from spbstu.exceptions import UnexpectedStatus

from .bot import get_bot

SLEEP_SECONDS = 30 * 60


async def __periodic_body(user_database: DictDatabase, send_message: Callable[[int, str], CoroutineType[Any, Any, Message]]) -> None:
    for chat_id_str in user_database.get_keys():
        chat_id: int = int(chat_id_str)
        user_code_str, spbstu_program_str = user_database.get(chat_id_str).split()

        try:
            user_index = await get_place_by_user_id(
                user_code=int(user_code_str),
                spbstu_program=int(spbstu_program_str)
            )
        except UnexpectedStatus as error:
            await send_message(chat_id, f"Ошибка:\n{error}")

        if user_index != -1:
            await send_message(chat_id, f"Ты ещё держишься! {user_index} место!")
            return

        await send_message(chat_id, "Бро... ты больше не в списках...")


async def periodic_message(bot: TelegramBot = get_bot(), user_database: DictDatabase = get_user_spbstu_db()) -> None:
    send_message = get_send_message(bot)

    while True:
        await __periodic_body(user_database, send_message)

        await sleep(SLEEP_SECONDS)
