from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from settings import Settings, get_settings
from spbstu import get_list_of_candidates_for_admission, UnexpectedStatus


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


# TODO
async def periodic_message(chat_id: int) -> None:
    ...


@dispatcher.message(Command("start"))
async def init(message: Message) -> None:
    await message.answer(
        "Ну шо, голова? Поехали",
        reply_markup=get_keyboard(
            text="На какой я позиции в списках к зачислению?"
        ).as_markup()
    )


@dispatcher.callback_query(F.data == "get_my_position")
async def get_my_position(callback: CallbackQuery, settings: Settings = get_settings()) -> None:
    try:
        data = await get_list_of_candidates_for_admission()
    except UnexpectedStatus as error:
        await callback_answer(str(error))
        return

    for index, candidate in enumerate(data):
        if int(candidate.code) == settings.spbstu_settings.id:
            await callback_answer(callback, f"Ты на {index + 1} месте!")
            return

    await callback_answer(callback, "Тебя нет в этом списке...")
