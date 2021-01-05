from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import bold, hbold

from database.database import User, Dish
from initialise import dp
from keyboards.inline_keyboard import menu_keyboard, category_keyboard

from states.states import Registration, OrderUser


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
            await registration_not_regtration_handler(message)
        elif is_active:
            await func(message)
        else:
            await message.answer("Пользователь не активен!")
    return wrapper


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
        pass # обновить пользователя
    # функция на сохранение юзера в bd
    await message.answer("Регистрация прошла успешно!")
    await state.finish()
    await main_menu_handler(message)


@dp.message_handler(commands=['start'])
@check_autorization
async def start_handler(message: types.Message):
    '''Bot entrypoint'''
    await message.answer("Приветствуем вас в телеграмм боте кафе София")
    await main_menu_handler(message)

# @dp.message_handler(content_types=['photo'])
# @check_autorization
# async def start_handler(message):
#     await message.photo[-1].download(f"photo/{message.photo[-1]['file_id']}.jpg")
#     await message.answer("Фото сохранено!")


@dp.message_handler(state=[OrderUser.start_order, None])
@check_autorization
async def main_menu_handler(message: types.Message):
    '''User main menu'''
    await message.answer(
        text=hbold("ГЛАВНОЕ МЕНЮ"),
        parse_mode='HTML',
        reply_markup=menu_keyboard
    )
    await OrderUser.start_order.set()


@dp.callback_query_handler(text=["change_user"], state=[OrderUser.start_order, None])
async def menu_handler(call: CallbackQuery, state: FSMContext):
    '''Go change informations about user'''
    await state.finish()
    await Registration.not_regtration.set()
    await registration_not_regtration_handler(call.message)


@dp.callback_query_handler(text=["menu", "to_menu"], state=OrderUser.start_order)
async def menu_handler(call: CallbackQuery):
    '''Select category'''
    await call.message.edit_text(
        text=hbold("ВЫБЕРИТЕ КАТЕГОРИЮ"),
        parse_mode='HTML'
    )
    await call.message.edit_reply_markup(reply_markup=category_keyboard)


@dp.callback_query_handler(text=["order_user"], state=OrderUser.start_order)
async def order_user_handler(call: CallbackQuery, state: FSMContext):
    '''Select category'''
    await call.message.edit_text(
        text=hbold("СПИСОК ЗАКАЗОВ"),
        parse_mode='HTML'
    )
    data = await state.get_data()
    if data:
        data_set = data.get("data_set")
        for val in data_set:
            await call.message.answer(
                text=val,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                    text="Убрать",
                    callback_data="remove_dish:{0}".format(val)
                )]])
            )
        await call.message.edit_reply_markup(
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                      text="Подтвердить заказ",
                                      callback_data="accept"
                                  )]]))
        await call.message.answer(
            text="Назад",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                text="Назад",
            callback_data="to_menu"
        )]]))
    else:
        await call.answer("Список заказов пуст!")
        await menu_handler(call)

@dp.callback_query_handler(text_startswith=["remove_dish"], state=OrderUser.start_order)
async def remove_dish_handler(call: CallbackQuery, state: FSMContext):
    dish = call.data.split(":")[1]
    data = await state.get_data()
    data_set = data.get("data_set")
    data_set.remove(dish)
    await state.update_data(data_set=data_set)
    await order_user_handler(call, state)


@dp.callback_query_handler(text="to_main_menu", state=OrderUser.start_order)
async def menu_handler_back(call: CallbackQuery):
    '''Back to the main menu'''
    await call.message.edit_reply_markup()
    await main_menu_handler(call.message)


@dp.callback_query_handler(text_startswith="dish", state=OrderUser.start_order)
async def dish_handler(call: CallbackQuery):
    '''Select dishes'''
    dish = call.data.split(':')[1]
    dishes = Dish.get_dishes(dish)
    await call.message.edit_text(
        text=hbold("Выберите блюдо"),
        parse_mode='HTML'
    )
    for val in dishes:
        if val.dish_photo:
            await call.message.answer_photo(photo=open(f"./photo/{val.dish_photo}", "rb"))
        await call.message.answer(text=f"Название: {val.dish_name}")
        await call.message.answer(text=f"Цена: {val.dish_price}р")
        await call.message.answer(
            text=f"Описание: {val.dish_description}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                text=f"Заказать {val.dish_name}",
                callback_data="add_dish:{0}".format(val.dish_name)
            )]])
        )
    await call.message.answer(
        text="Назад",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
            text="Назад",
            callback_data="to_menu")]])
    )


@dp.callback_query_handler(text_startswith="add_dish", state=OrderUser.start_order)
async def add_dish_handler(call: CallbackQuery, state: FSMContext):
    '''Select dishes'''
    dish = call.data.split(':')[1]
    data = await state.get_data()
    if data:
        data_set = data.get("data_set")
        data_set.add(dish)
    else:
        data_set = set()
        data_set.add(dish)
    await state.update_data(data_set=data_set)
    await call.answer(text="Блюдо {0} добавлено!".format(dish))