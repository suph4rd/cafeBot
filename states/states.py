from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    not_regtration = State()
    fio = State()
    phone_number = State()


class OrderUser(StatesGroup):
    start_order = State()