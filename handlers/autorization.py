from handlers.decorators import check_autorization
from aiogram import types
from aiogram.dispatcher import FSMContext
from database.database import User
from initialise import dp
from states.states import Registration


@dp.message_handler(commands=['start'])
@check_autorization
async def start_handler(message: types.Message):
    '''Bot entrypoint'''
    await message.answer("Приветствуем вас в телеграмм боте кафе София")
    from handlers import admin_handlers
    await admin_handlers.admin_main_menu_handler(message)


@dp.message_handler(state=Registration.not_regtration)
async def registration_not_regtration_handler(message):
    '''
    Enter personal data
    :param message: first name, last name and middle name
    '''
    await message.answer("Введите Фамилию Имя и Отчество (в одну строчку)")
    await Registration.fio.set()

@dp.message_handler(state=Registration.fio)
async def registration_fio_handler(message: types.Message, state: FSMContext):
    '''
    Enter phone number
    :param message: phone number
    :param state: current state of user
    '''
    await state.update_data(fio = message.text)
    await message.answer("Введите номер телефона")
    await Registration.phone_number.set()

@dp.message_handler(state=Registration.phone_number)
async def registration_phone_number_handler(message: types.Message, state: FSMContext):
    '''
    Create new user
    :param state: current state of user
    '''
    user = {
        "user_id": message['chat']['id'],
        "phone_number": message.text
            }
    data = await state.get_data()
    user["fio"] = data.get("fio")
    is_active = User.check_user_is_active(user["user_id"])
    if not is_active:
        User.create_user(user)
    else:
        User.update_user(user)
    await message.answer("Регистрация прошла успешно!")
    await state.finish()
    await admin_handlers.admin_main_menu_handler(message)