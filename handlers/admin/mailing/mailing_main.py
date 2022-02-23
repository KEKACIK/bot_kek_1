from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentTypes

from keyboards.inline.make_mailing_inline_kb import type_mailing_keyboard, mailing_cancel_keyboard
from loader import dp
from states.state import create_poll, mailing_text_state, mailing_photo_state, mailing_video_state


@dp.callback_query_handler(state='mailing_state')
async def mailing(call: CallbackQuery, state: FSMContext):
    value = call.data
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if value == 'mailing_poll':
        await call.bot.edit_message_text(chat_id=chat_id,
                                         message_id=message_id,
                                         text='\n'.join(["Создайте и отправьте сюда опрос, "
                                                         "также опрос будет рассылаться от вашего имени",
                                                         "Чтобы получить свежие данные перешлите опрос в любое место"]),
                                         reply_markup=mailing_cancel_keyboard)
        await create_poll.poll_massage_id.set()
    elif value == 'mailing_text':
        await call.bot.edit_message_text(chat_id=chat_id,
                                         message_id=message_id,
                                         text='\n'.join(["Вам необходимо ввести Текст одним сообщением",
                                                         "Весь текст будет использоваться в рассылке.",
                                                         "Вы можете использовать строчные смайлики."]),
                                         reply_markup=mailing_cancel_keyboard)
        await mailing_text_state.text.set()
    elif value == 'mailing_photo':
        await call.bot.edit_message_text(chat_id=chat_id,
                                         message_id=message_id,
                                         text='\n'.join(["Вам необходимо прислать Фото, затем Текст одним сообщением",
                                                         "Весь текст будет использоваться в рассылке.",
                                                         "Вы можете использовать строчные смайлики."]),
                                         reply_markup=mailing_cancel_keyboard)
        await mailing_photo_state.photo.set()
    elif value == 'mailing_video':
        await call.bot.edit_message_text(chat_id=chat_id,
                                         message_id=message_id,
                                         text='\n'.join(["Вам необходимо прислать Видео, затем Текст одним сообщением",
                                                         "Весь текст будет использоваться в рассылке.",
                                                         "Вы можете использовать строчные смайлики."]),
                                         reply_markup=mailing_cancel_keyboard)
        await mailing_video_state.video.set()


@dp.message_handler(state='mailing_state', content_types=ContentTypes.ANY)
async def mailing_text(message: Message, state: FSMContext):
    await message.bot.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.message_id - 1,
                                        text='Выберите из предложанных кнопок',
                                        reply_markup=type_mailing_keyboard)
    await message.delete()
