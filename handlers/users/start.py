from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.markdown import hbold

from loader import dp
from utils.db_api.db_categories import get_category
from utils.db_api.db_users import add_users, check_user


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    add_users(message)
    check = check_user(message)

    kb = []
    for cat in get_category():
        button = [InlineKeyboardButton(text=f"{cat}", callback_data=cat)]
        kb.append(button)
    cats_keyboard = InlineKeyboardMarkup(resize=True, inline_keyboard=kb)
    default_text = [
        f"📬 Приветствую, {hbold(message.chat.full_name)}!",
        f" ",
        f"<b>Я</b> - бот оптового сервиса <a href='https://onedropline.ru'><b>1drop</b></a>",
        f" ",
        f"Что я умею?",
        f"🔎 Умею находить ходовой товар по оптовой цене …"
    ]
    if check:
        default_text.extend([
            ' ',
            '<b>Но для начала, познакомимся?</b> 🤝'
        ])
        select_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
            [InlineKeyboardButton(text="🙅🏻‍♂️ Нет, спасибо!", callback_data='no_thankq'),
             InlineKeyboardButton(text="🙋🏻‍♂️Да, давай!", callback_data='opros')]
        ])
        await message.answer(text='\n'.join(default_text),
                             reply_markup=select_keyboard)
    else:
        default_text.extend([
            ' ',
            '👇🏼 <a>Выбери категорию</a> 👇🏼'
        ])
        await message.answer(
            text="\n".join(default_text),
            reply_markup=cats_keyboard
        )

    await state.set_state('choose_category_state')


@dp.callback_query_handler(text='cat_back')
async def cat_back(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot_start(call.message, state)
