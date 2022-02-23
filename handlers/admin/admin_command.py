import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

from data import config
from keyboards.inline.make_mailing_inline_kb import type_mailing_keyboard
from keyboards.inline.work_with_categories_inline_kb import work_with_cat_keyboard
from loader import dp

keyboards_admin_category = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📁 Работать категориями', callback_data='work_with_categories')],
    [InlineKeyboardButton(text='📤 Сделать рассылку', callback_data='make_mailing')],
    [InlineKeyboardButton(text='🗂 Выдать базу данных', callback_data='get_users')]
])


@dp.message_handler(Command('admin'), state='*')
async def admin(message: Message, state: FSMContext):
    if str(message.chat.id) in config.ADMINS:
        await message.answer("Выберите, что вы хотите сделать:",
                             reply_markup=keyboards_admin_category)
        await state.set_state("admin")
    else:
        await message.answer("Админ-панель доступна только админам.")


@dp.callback_query_handler(state='admin')
async def admin_category(call: CallbackQuery, state: FSMContext):
    category = call.data
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if category == 'work_with_categories':
        await call.bot.edit_message_text(message_id=message_id,
                                         chat_id=chat_id,
                                         text='Работать с категориями',
                                         reply_markup=work_with_cat_keyboard)
        await state.set_state('work_with_categories_state')

    elif category == 'make_mailing':
        await call.bot.edit_message_text(message_id=message_id,
                                         chat_id=chat_id,
                                         text='Выберите вид рассылки',
                                         reply_markup=type_mailing_keyboard)
        await state.set_state('mailing_state')
    elif category == 'get_users':
        logging.info(f"Пользователь {call.message.chat.full_name}({call.message.chat.id}) получил БД пользователей.")
        await call.bot.send_document(chat_id=chat_id, document=open("Users_2.xlsx", 'rb'))
        await call.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await state.finish()
