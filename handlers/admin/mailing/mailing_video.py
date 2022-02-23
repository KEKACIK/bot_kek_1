from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentTypes

from handlers.admin.admin_command import admin
from keyboards.inline.make_mailing_inline_kb import submit_keyboard, mailing_cancel_keyboard
from loader import dp
from states.state import mailing_video_state
from utils.db_api.db_users import get_users


@dp.message_handler(state=mailing_video_state.video, content_types=ContentTypes.VIDEO)
async def photo_mailing_video(message: Message, state: FSMContext):
    video_id = message.video.file_id
    await state.update_data({'video_id': video_id})
    await message.answer(text="\n".join(["Теперь пришлите текст для рассылки.",
                                         "Чтобы пропустить пришлите точку ' . '"]),
                         reply_markup=mailing_cancel_keyboard)
    await mailing_video_state.text.set()


@dp.message_handler(state=mailing_video_state.text)
async def photo_mailing_text(message: Message, state: FSMContext):
    data = await state.get_data()
    data['text'] = message.text
    await state.update_data(data)
    if data['text'] == '.':
        await message.bot.send_video(chat_id=message.chat.id,
                                     video=data['video_id'])
    else:
        await message.bot.send_video(chat_id=message.chat.id,
                                     video=data['video_id'],
                                     caption=data['text'])
    await message.answer(text="Проверьте всё ли верно перед отправкой.",
                         reply_markup=submit_keyboard)
    await mailing_video_state.submit.set()


@dp.callback_query_handler(state=mailing_video_state.submit)
async def text_submit(call: CallbackQuery, state: FSMContext):
    if call.data == 'submit':
        users_id = get_users()
        data = await state.get_data()
        k = 0
        if data['text'] == '.':
            for user_id in users_id:
                try:
                    await call.bot.send_video(chat_id=user_id,
                                              video=data['video_id'])
                    k += 1
                except:
                    pass
        else:
            for user_id in users_id:
                try:
                    await call.bot.send_video(chat_id=user_id,
                                              video=data['video_id'],
                                              caption=data['text'])
                    k += 1
                except:
                    pass
        await call.bot.edit_message_text(chat_id=call.message.chat.id,
                                         message_id=call.message.message_id,
                                         text=f"Сообщение разослано {k}/{len(users_id)}")
        await state.finish()
    elif call.data == 'cancel':
        await call.bot.send_message(chat_id=call.message.chat.id,
                                    text='Действие отменено.\n'
                                         '/admin - Админ-панель\n'
                                         '/start')
        await state.finish()


@dp.message_handler(state=mailing_video_state.video, content_types=ContentTypes.ANY)
async def photo_mailing_photo_dt_photo(message: Message, state: FSMContext):
    try:
        await message.bot.edit_message_text(chat_id=message.chat.id,
                                            message_id=message.message_id - 1,
                                            text='Сейчас нужно прислать видеозапись',
                                            reply_markup=mailing_cancel_keyboard)
    except:
        pass
    await message.delete()


@dp.message_handler(state=mailing_video_state.text, content_types=ContentTypes.ANY)
async def photo_mailing_photo_dt_text(message: Message, state: FSMContext):
    await message.bot.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.message_id - 1,
                                        text='Сейчас нужно прислать текст или точку',
                                        reply_markup=mailing_cancel_keyboard)
    await message.delete()


@dp.message_handler(state=mailing_video_state.submit, content_types=ContentTypes.ANY)
async def photo_mailing_photo_dt_btn(message: Message, state: FSMContext):
    await message.bot.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.message_id - 1,
                                        text='Выберите из предложанных кнопок',
                                        reply_markup=submit_keyboard)
    await message.delete()


@dp.callback_query_handler(state=mailing_video_state)
async def exit(call: CallbackQuery, state: FSMContext):
    await admin(call.message, state)
