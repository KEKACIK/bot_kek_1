import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentTypes, InlineKeyboardButton, InlineKeyboardMarkup

from handlers.users.category_h import choose_category
from keyboards.inline.informations_inline_kb import q1_keyboard_raw, q2_keyboard_raw, q3_keyboard_raw, \
    submit_keyboard_raw
from loader import dp
from states.state import informations_state
from utils.db_api.db_users import info_sub


@dp.callback_query_handler(state=informations_state.Q1_marketplays)
async def info_select_Q1(call: CallbackQuery, state: FSMContext):
    #   keyboard from q1_selected
    text = ['Вопрос 1️⃣ / 3️⃣:',
            'На каких площадках вы торгуете?']
    for raw in q1_keyboard_raw:
        if call.data == raw:
            text.append(f"✅ {raw}")
        else:
            text.append(f"☑️  {raw}")
    #   keyboard from q2
    kb = []
    for raw in q2_keyboard_raw:
        kb.append([InlineKeyboardButton(text=f"☑️  {raw}", callback_data=q2_keyboard_raw[raw])])
    data = await state.get_data()
    data['Q1_id'] = call.message.message_id
    data['Q1'] = call.data
    await state.update_data(data)
    await call.bot.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=data['Q1_id'],
                                     text='\n'.join(text))
    await call.message.answer(text='\n'.join(['Вопрос 2⃣ / 3️⃣:',
                                              'Какой ваш оборот месяц?']),
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
    await informations_state.Q2_earning.set()


@dp.callback_query_handler(state=informations_state.Q2_earning)
async def info_select_Q2(call: CallbackQuery, state: FSMContext):
    #   keyboard from q2_selected
    text = ['Вопрос 2️⃣ / 3️⃣:',
            'Какой ваш оборот месяц?']
    for raw in q2_keyboard_raw:
        if call.data == raw:
            text.append(f"✅ {raw}")
        else:
            text.append(f"☑️  {raw}")
    #   keyboard from q3
    kb = []
    for raw in q3_keyboard_raw:
        kb.append([InlineKeyboardButton(text=f"☑️  {raw}", callback_data=q3_keyboard_raw[raw])])
    data = await state.get_data()
    data['Q2_id'] = call.message.message_id
    data['Q2'] = call.data
    await state.update_data(data)
    await call.bot.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=data['Q2_id'],
                                     text='\n'.join(text))
    await call.message.answer(text='\n'.join(['Вопрос 3️⃣ / 3️⃣:',
                                              'Выберите/Напишите откуда вы?']),
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
    await informations_state.Q3_city.set()


async def info_select_Q3_universal(state: FSMContext, call: CallbackQuery = None, message: Message = None):
    data = await state.get_data()
    if call is not None:
        user_mess = call.data
    else:
        user_mess = message.text
    #   keyboard from q3_selected
    text = ['Вопрос 3️⃣ / 3️⃣:',
            'Выберите/Напишите откуда вы?']
    ok = True
    for raw in q3_keyboard_raw:
        if user_mess == raw:
            text.append(f"✅ {raw}")
            ok = False
        else:
            text.append(f"☑️  {raw}")
    if ok:
        text.append(f"✅ {user_mess}")
    #   keyboard from select
    kb = []
    for raw in submit_keyboard_raw:
        kb.append([InlineKeyboardButton(text=f"{raw}", callback_data=submit_keyboard_raw[raw])])
    if call is not None:
        await call.bot.edit_message_text(chat_id=call.message.chat.id,
                                         message_id=data['Q3_id'],
                                         text='\n'.join(text))
        await call.message.answer(text='\n'.join([f"Всё ли правильно я понял?",
                                                  f"📦 : {data['Q1']}",
                                                  f"🔄 : {data['Q2']}",
                                                  f"📍: {data['Q3']}"]),
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
    elif message is not None:
        await message.delete()
        await message.bot.edit_message_text(chat_id=message.chat.id,
                                            message_id=data['Q3_id'],
                                            text='\n'.join(text))
        await message.answer(text='\n'.join([f"Всё ли правильно я понял?",
                                             f"📦 : {data['Q1']}",
                                             f"🔄 : {data['Q2']}",
                                             f"📍: {data['Q3']}"]),
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
    await informations_state.submit.set()


@dp.callback_query_handler(state=informations_state.Q3_city)
async def info_select_Q3(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data['Q3_id'] = call.message.message_id
    data['Q3'] = call.data
    await state.update_data(data)
    await info_select_Q3_universal(call=call, state=state)


@dp.message_handler(state=informations_state.Q3_city)
async def info_select_Q3_text(message: Message, state: FSMContext):
    data = await state.get_data()
    data['Q3_id'] = message.message_id - 1
    data['Q3'] = message.text.capitalize()
    await state.update_data(data)
    await info_select_Q3_universal(message=message, state=state)


@dp.callback_query_handler(state=informations_state.submit)
async def info_submit(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    for i in range(int(data['Q1_id']), call.message.message_id + 1):
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=i)
        except:
            pass
    if call.data == 'submit':
        message = call.message
        info_sub(message, data)
        await call.message.answer(text='Рад с тобой познакомится! 🥰\n'
                                       '/start - чтобы получить начальный список')
        await state.finish()
    else:
        logging.info(f"Пользователь {call.message.chat.full_name}({call.message.chat.id}), перепроходит опрос.")
        call_t = call
        call_t['data'] = 'opros'
        await choose_category(call_t, state)


@dp.message_handler(state=informations_state, content_types=ContentTypes.ANY)
async def photo_mailing_photo_dt_btn(message: Message, state: FSMContext):
    await message.answer(text='Выберите из предложанных кнопок')
    await message.delete()
