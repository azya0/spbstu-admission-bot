from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyMarkupUnion
from aiogram.utils.keyboard import InlineKeyboardBuilder
from rapidfuzz import fuzz, process

from database import DictDatabase
from database.redis_database import get_user_spbstu_db
from spbstu import UnexpectedStatus
from spbstu.endpoints import get_list_of_programs, get_place_by_user_id

dispatcher = Dispatcher()


def get_keyboard(text: str) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(
        text=text,
        callback_data="get_my_position"
    )

    return keyboard


async def callback_answer(
    callback: CallbackQuery,
    text: str,
    reply_markup: ReplyMarkupUnion | None = get_keyboard("Обновить").as_markup()
) -> None:
    await callback.message.answer(text, reply_markup=reply_markup)
    await callback.answer()


class Form(StatesGroup):
    search_program_code = State()
    set_user_code = State()
    main_state = State()


@dispatcher.message(Command("start"))
async def init(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Ну шо, голова? Поехали!\n\nКак твоё направление там называлось? Напиши, я поищу",
    )

    await state.set_state(Form.search_program_code)


@dispatcher.message(Form.search_program_code)
async def process_program_code(message: Message, state: FSMContext) -> None:
    programs = await get_list_of_programs()

    results = process.extract(
        message.text,
        tuple(program.title for program in programs),
        scorer=fuzz.WRatio,
        limit=1,
        score_cutoff=60
    )

    if not results:
        await message.answer(text="Даже близко такой фигни не нашёл\n\nДавай по новой")
        return

    title, _, index = results[0]
    
    await state.update_data(program_id=programs[index].id)

    keyboard = InlineKeyboardBuilder()
        
    keyboard.button(
        text="Подтвердить",
        callback_data="verify_program_title"
    )

    await message.answer(
        text=f"Нашёл:\n\n{title}",
        reply_markup=keyboard.as_markup()
    )


@dispatcher.callback_query(F.data == "verify_program_title")
async def verify_program(callback: CallbackQuery, state: FSMContext) -> None:
    await callback_answer(
        callback,
        text="Норм. А код у тебя какой?\n\nЯ по нему буду искать тебя в таблицах, так что не проебись",
        reply_markup=None
    )

    await state.set_state(Form.set_user_code)


@dispatcher.message(Form.set_user_code)
async def set_user_code(
    message: Message,
    state: FSMContext,
    user_database: DictDatabase = get_user_spbstu_db()
) -> None:
    if message.text is None:
        await message.answer("Каво? Попробуй ещё раз")
        return

    if not message.text.isdigit():
        await message.answer("Твой код должен быть числом. Попробуй ещё раз")
        return

    await state.update_data(user_id=int(message.text))

    user_database.set(
        key=str(message.chat.id),
        value=f"{message.text} {(await state.get_data())["program_id"]}"
    )

    await state.set_state(Form.main_state)

    await main_state(message, state)


@dispatcher.message(Form.main_state)
async def main_state(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    try:
        index = await get_place_by_user_id(
            user_code=data["user_id"],
            spbstu_program=data["program_id"]
        )
    except UnexpectedStatus:
        await message.answer("Ну я тут погуглил... Нихуя я не нагуглил, пиздец какой-то")

    if index == -1:
        await message.answer('Тебя там нету со статусом "К зачислению"...')

    await message.answer(
        f"Ну я тут погуглил... Ты короче на {index} месте",
        reply_markup=get_keyboard(text="Обновить").as_markup()
    )


@dispatcher.callback_query(F.data == "get_my_position")
async def get_my_position(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    
    try:
        index = await get_place_by_user_id(
            user_code=data["user_id"],
            spbstu_program=data["program_id"]
        )
    except UnexpectedStatus as error:
        await callback_answer(str(error))
        return

    if index != -1:
        await callback_answer(callback, f"Ты на {index} месте!")
        return

    await callback_answer(callback, "Тебя нет в этом списке...")
