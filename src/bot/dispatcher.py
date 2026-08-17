from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import DictDatabase
from database.redis_database.database import get_user_db
from spbstu import UnexpectedStatus
from spbstu.endpoints import get_place_by_user_id


dispatcher = Dispatcher()


def get_keyboard(text: str) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(
        text=text,
        callback_data="get_my_position"
    )

    return keyboard


async def callback_answer(callback: CallbackQuery, text: str) -> None:
    await callback.message.answer(text, reply_markup=get_keyboard("Обновить").as_markup())
    await callback.answer()


@dispatcher.message(Command("start"))
async def init(message: Message, user_database: DictDatabase = get_user_db()) -> None:
    if message.from_user is not None:
        user_database.set(str(message.from_user.id), str(message.chat.id))

    await message.answer(
        "Ну шо, голова? Поехали",
        reply_markup=get_keyboard(
            text="На какой я позиции в списках к зачислению?"
        ).as_markup()
    )


@dispatcher.callback_query(F.data == "get_my_position")
async def get_my_position(callback: CallbackQuery) -> None:
    try:
        index = await get_place_by_user_id()
    except UnexpectedStatus as error:
        await callback_answer(str(error))
        return

    if index != -1:
        await callback_answer(callback, f"Ты на {index} месте!")
        return

    await callback_answer(callback, "Тебя нет в этом списке...")
