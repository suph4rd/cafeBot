from config import ADMIN_ID
from database.database import User
import handlers.autorization as autorization
from states.states import Registration
import handlers.user_handlers as user_handlers


def check_autorization(func):
    '''
    Decorator for autorization and registration
    :param func: handler_funcrion
    '''
    async def wrapper(message):
        user_id = message['chat']['id']
        exists = User.check_user_exists(user_id)
        is_active = User.check_user_is_active(user_id)
        if not exists:
            await Registration.not_regtration.set()
            await autorization.registration_not_regtration_handler(message)
        elif is_active:
            await func(message)
        else:
            await message.answer("Пользователь не активен!")
    return wrapper


def check_admin(func):
    '''
    Decorator is check admin status of user
    :param func: handler_funcrion
    '''
    async def wrapper(message):
        user_id = message['chat']['id']
        if user_id == ADMIN_ID:
            await func(message)
        else:
            await user_handlers.main_menu_handler(message)
    return wrapper