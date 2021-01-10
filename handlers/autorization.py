from handlers.decorators import check_authorization
from aiogram import types
from aiogram.dispatcher import FSMContext
from database.database import User
from initialise import dp
from states.states import Registration


@dp.message_handler(commands=['start'])
@check_authorization
async def start_handler(message: types.Message, *args, **kwargs):
    '''Bot entrypoint'''
    await message.answer("Приветствуем вас в телеграмм боте кафе София")
    from handlers import admin_handlers
    await admin_handlers.admin_main_menu_handler(message)


@dp.message_handler(state=Registration.not_registration)
async def registration_not_registration_handler(message: types.Message, *args, **kwargs):
    '''
    Enter personal data
    :param message: first name, last name and middle name
    '''
    user_dict = {}
    user_id = int(kwargs.get("user_id")) if kwargs.get("user_id") else message['chat']['id']
    if user_id:
        user_db = User.get_user(user_id)
        user_dict = {
            "fio": user_db.fio,
            "phone_number": user_db.phone_number
        }
    user_dict['user_id'] = user_id
    if user_dict.get('fio'):
        await message.answer("Введите новые Фамилию Имя и Отчество (в одну строчку)")
        await message.answer(f"Текущие: {user_dict.get('fio')}")
    else:
        await message.answer("Введите Фамилию Имя и Отчество (в одну строчку)")
    await Registration.fio.set()
    state = dp.current_state()
    await state.update_data(user_dict=user_dict)


@dp.message_handler(state=Registration.fio)
async def registration_fio_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    '''
    Enter phone number
    :param message: phone number
    :param state: current state of user
    '''
    data = await state.get_data()
    user_dict = data.get("user_dict")
    user_dict['fio'] = message.text
    await state.update_data(user_dict=user_dict)
    if user_dict.get('phone_number'):
        await message.answer("Введите новый номер телефона")
        await message.answer(f"Текущий:{user_dict.get('phone_number')}")
    else:
        await message.answer("Введите номер телефона")
    await Registration.phone_number.set()


@dp.message_handler(state=Registration.phone_number)
async def registration_phone_number_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    '''
    Create new user
    :param state: current state of user
    '''
    data = await state.get_data()
    user_dict = data.get("user_dict")
    user_dict['phone_number'] = message.text
    is_active = User.check_user_is_active(user_dict["user_id"])
    if not is_active:
        User.create_user(user_dict)
        await message.answer("Регистрация прошла успешно!")
    else:
        User.update_user(user_dict)
        await message.answer("Изменения приняты!")
    await state.finish()
    from handlers import admin_handlers
    await admin_handlers.admin_main_menu_handler(message)
