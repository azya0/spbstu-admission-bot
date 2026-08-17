import asyncio

from aiogram import Bot as TelegramBot

from .newsletter import periodic_message

from .bot import get_bot
from .dispatcher import dispatcher


async def run(bot: TelegramBot = get_bot()) -> None:
    await asyncio.gather(
        dispatcher.start_polling(bot),
        periodic_message(),
    )
