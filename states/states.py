from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    not_registration = State()
    fio = State()
    phone_number = State()


class OrderUser(StatesGroup):
    start_order = State()


class ChangeTemplate(StatesGroup):
    start = State()
    add_category = State()
    add_template = State()
