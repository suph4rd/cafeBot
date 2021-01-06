from config import ADMIN_ID
from database.database import User
from states.states import Registration


def check_authorization(func):
    '''
    Decorator for authorization and registration
    :param func: handler_function
    '''
    async def wrapper(message):
        user_id = message['chat']['id']
        exists = User.check_user_exists(user_id)
        is_active = User.check_user_is_active(user_id)
        if not exists:
            await Registration.not_regtration.set()
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
        user_id = message['chat']['id']
        if user_id == ADMIN_ID:
            await func(message)
        else:
            from handlers.user_handlers import main_menu_handler
            await main_menu_handler(message)
    return wrapper