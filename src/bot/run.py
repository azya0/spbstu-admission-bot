from aiogram import Bot as TelegramBot

from .bot import get_bot
from .dispatcher import dispatcher


async def run(bot: TelegramBot = get_bot()) -> None:
    await dispatcher.start_polling(bot)
