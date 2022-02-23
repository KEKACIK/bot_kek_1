import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from handlers.users.start import bot_start
from keyboards.inline.informations_inline_kb import q1_keyboard_raw
from loader import dp
from states.state import informations_state
from utils.db_api.db_categories import get_category
from utils.db_api.db_users import info_sub


@dp.callback_query_handler(state='choose_category_state')
async def choose_category(call: CallbackQuery, state: FSMContext):
    if call.data == 'opros':
        logging.info(f"Пользователь {call.message.chat.full_name}({call.message.chat.id}), начал прохождение опроса")
        kb = []
        for raw in q1_keyboard_raw:
            kb.append([InlineKeyboardButton(text=f"☑️  {raw}", callback_data=q1_keyboard_raw[raw])])
        try:
            await call.bot.edit_message_text(chat_id=call.message.chat.id,
                                             message_id=call.message.message_id,
                                             text='Вопрос 1️⃣ / 3️⃣:\n'
                                                  'На каких площадках вы торгуете?',
                                             reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
        except:
            await call.bot.send_message(chat_id=call.message.chat.id,
                                        text='Вопрос 1️⃣ / 3️⃣:\n'
                                             'На каких площадках вы торгуете?',
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
        await informations_state.Q1_marketplays.set()
        return
    elif call.data == 'no_thankq':
        await call.message.delete()
        logging.info(f"Пользователь {call.message.chat.full_name}({call.message.chat.id}), отказался от опроса")
        info_sub(call.message, {'Q1': '-', 'Q2': '-', 'Q3': '-'})
        await bot_start(call.message, state)
        return
    category = call.data
    cats = get_category()
    keyboards_link = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Назад', callback_data='cat_back'),
         InlineKeyboardButton(text='Открыть 🔜', url=cats[category])]
    ])
    await call.bot.send_message(chat_id=call.message.chat.id,
                                text='\n'.join([f"Выбрана категория:",
                                                f" ",
                                                f"✅ {category}"]),
                                reply_markup=keyboards_link)
    await call.message.delete()
    await state.finish()
