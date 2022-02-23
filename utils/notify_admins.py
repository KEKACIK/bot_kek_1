import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "💫 Бот Запущен 💫\n"
                                             "/admin - для использования админ-панели\n"
                                             "/start - для использования юсер-панели")

        except Exception as err:
            logging.exception(err)
