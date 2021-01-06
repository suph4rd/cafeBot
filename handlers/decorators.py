from database.database import User
import handlers.autorization as autorization
from states.states import Registration


def check_autorization(func):
    '''
    Decorator for autorization and registration
    :param func: handler_funcrion
    '''
    async def wrapper(message):
        user_id = message['chat']['id']
        exists = User.check_user_exists(user_id)
        is_active = User.check_user_is_active(user_id)   # проверить по user_id активен ли пользователь
        if not exists:
            await Registration.not_regtration.set()
            await autorization.registration_not_regtration_handler(message)
        elif is_active:
            await func(message)
        else:
            await message.answer("Пользователь не активен!")
    return wrapper