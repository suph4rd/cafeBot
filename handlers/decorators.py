import aiogram
from config import ADMIN_ID
from database.database import User, OrderList
from states.states import Registration


def get_user_id(message):
    '''
    Function for decorators
    :return: user_id for decorators
    '''
    if isinstance(message, aiogram.types.callback_query.CallbackQuery):
        user_id = message['from']['id']
    else:
        user_id = message['chat']['id']
    return user_id


def check_authorization(func):
    '''
    Decorator for authorization and registration
    :param func: handler_function
    '''
    async def wrapper(message):
        user_id = get_user_id(message)
        exists = User.check_user_exists(user_id)
        is_active = User.check_user_is_active(user_id)
        if not exists:
            await Registration.not_registration.set()
            from handlers.autorization import registration_not_registration_handler
            await registration_not_registration_handler(message)
        elif is_active:
            await func(message)
        else:
            await message.answer("Пользователь не активен!")
    return wrapper


def check_admin(func):
    '''
    Decorator is check admin status of user
    :param func: handler_function
    '''
    async def wrapper(message):
        user_id = get_user_id(message)
        if user_id == ADMIN_ID:
            await func(message)
        else:
            from handlers.user_handlers import main_menu_handler
            await main_menu_handler(message)
    return wrapper


def check_order_today(func):
    '''
    checks if the user made an order today
    '''
    async def wrapper(message, **kwargs):
        user_id = get_user_id(message)
        state = kwargs.get("state")
        is_order = OrderList.check_order_today(user_id)
        if is_order:
            await message.answer("Извените, но вы уже сделали заказ на сегодня! Приходите завтра!")
        else:
            await func(message, state) if state else await func(message)
    return wrapper
