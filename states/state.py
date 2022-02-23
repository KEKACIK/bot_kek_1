from aiogram.dispatcher.filters.state import StatesGroup, State


class add_category(StatesGroup):
    category_name = State()
    category_link = State()


class create_poll(StatesGroup):
    poll_massage_id = State()
    submit = State()


class mailing_text_state(StatesGroup):
    text = State()
    submit = State()


class mailing_photo_state(StatesGroup):
    photo = State()
    text = State()
    submit = State()


class mailing_video_state(StatesGroup):
    video = State()
    text = State()
    submit = State()


class informations_state(StatesGroup):
    Q1_marketplays = State()
    Q2_earning = State()
    Q3_city = State()
    submit = State()


