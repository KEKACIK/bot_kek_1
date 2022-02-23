from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

work_with_cat_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Добавить категорию', callback_data='add_category'),
        InlineKeyboardButton(text='Удалить категорию', callback_data='delete_category')
    ],
    [
        InlineKeyboardButton(text='Выйти', callback_data='cancel')
    ]
])

make_mailing_keyboard = InlineKeyboardMarkup(inline_keyboard=[

])
