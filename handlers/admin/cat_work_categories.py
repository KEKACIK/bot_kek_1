from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp
from states.state import add_category
from utils.db_api.db_categories import get_category


@dp.callback_query_handler(state='work_with_categories_state')
async def work_with_categories(call: CallbackQuery, state=FSMContext):
    values = call.data
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if values == 'add_category':
        await call.bot.edit_message_text(
            message_id=message_id,
            chat_id=chat_id,
            text="Введите название категории:"
        )
        await add_category.category_name.set()  # Перебрасывает нас на следующий уровень (в add_category_name)
    elif values == 'delete_category':
        items = get_category()
        kb = []
        for item in items:
            kb.append([InlineKeyboardButton(text=item, callback_data=item)])
        kb.append([InlineKeyboardButton(text='Отменить', callback_data='cancel')])
        keyboards = InlineKeyboardMarkup(row_width=1, inline_keyboard=kb)
        await call.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Выберите категорию для удаления",
            reply_markup=keyboards
        )
        await state.set_state('delete_category_state')
    elif values == 'cancel':
        await call.bot.edit_message_text(chat_id=chat_id,
                                         message_id=message_id,
                                         text="Вы вышли из панели администратора.\n"
                                              "/start - чтобы пользоваться ботом\n"
                                              "/admin - чтобы войти в панель администратора")
        await state.finish()
