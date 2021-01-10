from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    start = State()
    not_registration = State()
    fio = State()
    phone_number = State()


class OrderUser(StatesGroup):
    start_order = State()