from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp
from utils.db_api.db_categories import get_category, create_category


@dp.callback_query_handler(state='delete_category_state')
async def delete_category(call: CallbackQuery, state: FSMContext):
    value = call.data
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if value == 'cancel':
        await call.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Действие отменено.\n"
                 "/admin - чтобы войти в панель администратора"
        )
        await state.finish()
        return
    data = get_category()
    data.pop(value)
    create_category(data)
    await call.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"Категория под названием '{value}', успешно удалена"
    )
    await state.finish()
