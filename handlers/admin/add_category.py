from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp
from states.state import add_category
from utils.db_api.db_categories import get_category, create_category


@dp.message_handler(state=add_category.category_name)
async def add_category_name(message: Message, state: FSMContext):
    chat_id = message.chat.id
    message_id = message.message_id - 1
    cat_name = message.text
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"Введите ссылку для категории '{cat_name}':"
    )
    await message.delete()
    await state.update_data({
        'category_name': cat_name,
        'message_id': message_id
    })
    await add_category.category_link.set()


@dp.message_handler(state=add_category.category_link)
async def add_category_link(message: Message, state: FSMContext):
    data = await state.get_data('category_name')
    chat_id = message.chat.id
    message_id = data['message_id']
    # Получение данных из Стейта
    data = await state.get_data('category_name')
    cat_name = data['category_name']
    cat_link = message.text
    # Получение и изменение БД (гыг)
    data = get_category()
    data[cat_name] = cat_link
    create_category(data)
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"Категория с названием '{cat_name}'\n"
             f"и ссылкой: '{cat_link}'\n"
             f"создана, поздравляю"
    )
    await message.delete()
    await state.finish()
