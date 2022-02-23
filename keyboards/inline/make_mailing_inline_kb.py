from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, inline_keyboard
from aiogram.utils import callback_data

type_mailing_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Опрос', callback_data='mailing_poll'),
        InlineKeyboardButton(text='Текст', callback_data='mailing_text')
    ],
    [
        InlineKeyboardButton(text='Фото с текстом', callback_data='mailing_photo'),
        InlineKeyboardButton(text='Видео с текстом', callback_data='mailing_video')
    ],
])


submit_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Всё проверил отсылай', callback_data='submit')],
    [InlineKeyboardButton(text='Отменить', callback_data='cancel')]
])


mailing_cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Выйти", callback_data='exit')]
])


