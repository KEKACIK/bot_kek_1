import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, ContentTypes

from data import config
from loader import dp
# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
from utils.db_api.db_categories import get_category


@dp.message_handler(state=None)
async def bot_echo(message: Message):
    logging.info(f"Кто-то попал в ловушку {message}")
    if str(message.chat.id) in config.ADMINS:
        await message.answer("Извини,я не понимаю, используйте команду ещё раз\n"
                             "/start - юзер-панель\n",
                             "/admin - админ-панель")
    else:
        await message.answer("Извини,я не понимаю, используйте команду ещё раз\n"
                             "/start - для использования бота")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=ContentTypes.ANY)
async def bot_echo_all(message: Message, state: FSMContext):
    await bot_echo(message)
    await state.finish()


@dp.callback_query_handler()
async def echo_call(call: CallbackQuery, state: FSMContext):
    await call.bot.edit_message_text(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     text="Используйте /start, для работы с ботом")
    # chat_id = call.message.chat.id
    # message_id = call.message.message_id
    # cats = get_category()
    # kb = []
    # for cat in cats:
    #     button = [InlineKeyboardButton(text=cat, callback_data=cat)]
    #     kb.append(button)
    # cats_keyboard = InlineKeyboardMarkup(resize=True, inline_keyboard=kb)
    # await call.bot.send_message(
    #     chat_id=chat_id,
    #     text="\n".join([f"Приветствую, {call.message.from_user.full_name}!",
    #                     f"Я бот оптового сервиса OneDrop.",
    #                     f"Для заказа просто выбери интересующую категорию и бот подскажет сайт,",
    #                     f"где можно заказать этот товар."]),
    #     reply_markup=cats_keyboard)
    # await call.bot.delete_message(chat_id=chat_id, message_id=message_id)
    # await state.set_state('choose_category_state')
