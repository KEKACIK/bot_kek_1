from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from handlers.admin.admin_command import admin
from keyboards.inline.make_mailing_inline_kb import submit_keyboard, mailing_cancel_keyboard
from loader import dp
from states.state import create_poll
from utils.db_api.db_users import get_users


@dp.message_handler(state=create_poll.poll_massage_id, content_types=ContentTypes.POLL)
async def mailing_forward_pool(message: Message, state: FSMContext):
    chat_id = message.chat.id
    message_id = message.message_id
    await state.update_data({
        'message_id': message_id,
        'chat_id': chat_id
    })
    await message.bot.forward_message(chat_id=chat_id,
                                      message_id=message_id,
                                      from_chat_id=chat_id)
    await message.answer(text="Проверьте всё ли верно перед отправкой.",
                         reply_markup=submit_keyboard)
    await create_poll.submit.set()


@dp.callback_query_handler(state=create_poll.submit)
async def submit(call: CallbackQuery, state: FSMContext):
    value = call.data
    if value == 'submit':
        users_id = get_users()
        data = await state.get_data('poll_massage_id')
        chat_id = data['chat_id']
        message_id = data['message_id']
        k = 0
        for user_id in users_id:
            try:
                await call.message.bot.forward_message(chat_id=user_id,
                                                       from_chat_id=chat_id,
                                                       message_id=message_id)
                k += 1
            except:
                pass
        await call.message.reply(text=f"Сообщение разослано {k}/{len(users_id)}")
        await state.finish()


@dp.message_handler(state=create_poll.poll_massage_id, content_types=ContentTypes.ANY)
async def photo_mailing_photo_dt_text(message: Message, state: FSMContext):
    await message.bot.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.message_id - 1,
                                        text='Сейчас нужно прислать опрос',
                                        reply_markup=mailing_cancel_keyboard)
    await message.delete()


@dp.message_handler(state=create_poll.submit, content_types=ContentTypes.ANY)
async def photo_mailing_photo_dt_btn(message: Message, state: FSMContext):
    await message.bot.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.message_id - 1,
                                        text='Выберите из предложанных кнопок',
                                        reply_markup=submit_keyboard)
    await message.delete()


@dp.callback_query_handler(state=create_poll)
async def exit(call: CallbackQuery, state: FSMContext):
    await admin(call.message, state)

