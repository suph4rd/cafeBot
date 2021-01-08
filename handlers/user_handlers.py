import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold
from config import ADMIN_ID
from database.database import Dish, OrderList
from handlers import admin_handlers, autorization
from handlers.decorators import check_authorization, check_order_today, get_user_id
from initialise import dp
from keyboards.inline_keyboard import menu_keyboard, get_inline_keyboard_markup, \
    get_category_keyboard
from states.states import Registration, OrderUser


@dp.message_handler(state=[OrderUser.start_order, None])
@check_authorization
async def main_menu_handler(message: types.Message, *args, **kwargs):
    '''User main menu'''
    message = message.message if isinstance(message, aiogram.types.callback_query.CallbackQuery) else message
    user_id = get_user_id(message)
    if user_id == ADMIN_ID:
        await admin_handlers.admin_main_menu_handler(message)
    else:
        await message.answer(
            text=hbold("ГЛАВНОЕ МЕНЮ"),
            reply_markup=menu_keyboard
        )
        await OrderUser.start_order.set()


@dp.callback_query_handler(text=["change_user"], state=[OrderUser.start_order, None])
async def change_user_handler(call: CallbackQuery, state: FSMContext, *args, **kwargs):
    '''Go change information about user'''
    await state.finish()
    await Registration.not_regtration.set()
    await autorization.registration_not_registration_handler(call.message)


@dp.callback_query_handler(text=["menu", "to_menu"], state=OrderUser.start_order)
@check_order_today
async def menu_handler(call: CallbackQuery, *args, **kwargs):
    '''Select category'''
    user_id = get_user_id(call)
    is_order = OrderList.check_order_today(user_id)
    if is_order:
        await call.answer("Извените, но вы уже сделали заказ на сегодня! Приходите завтра!")
        await main_menu_handler(call.message)
    else:
        await call.message.edit_text(text=hbold("ВЫБЕРИТЕ КАТЕГОРИЮ"))
        await call.message.edit_reply_markup(reply_markup=get_category_keyboard())


@dp.callback_query_handler(text=["order_user"], state=OrderUser.start_order)
@check_order_today
async def order_user_handler(call: CallbackQuery, state: FSMContext, *args, **kwargs):
    '''Select category'''
    data = await state.get_data()
    if data.get("data_set"):
        await call.message.edit_text(text=hbold("СПИСОК ЗАКАЗОВ"))
        data_set = data.get("data_set")
        for val in data_set:
            await call.message.answer(
                text=val,
                reply_markup=get_inline_keyboard_markup(
                    text=f"Убрать {val}",
                    callback_data="remove_dish:{0}".format(val)
                )
            )
        await call.message.edit_reply_markup(
                                  reply_markup=get_inline_keyboard_markup(
                                      text="Подтвердить заказ",
                                      callback_data="accept_order"
                                  )
        )
        await call.message.answer(
            text="Назад",
            reply_markup=get_inline_keyboard_markup(
                text="Назад",
                callback_data="to_menu"
            )
        )
    else:
        await call.answer("Список заказов пуст!")


@dp.callback_query_handler(text_startswith=["accept_order"], state=OrderUser.start_order)
@check_order_today
async def accept_order_handler(call: CallbackQuery, state: FSMContext, *args, **kwargs):
    data = await state.get_data()
    data_set = data.get("data_set")
    if data_set:
        user_id = get_user_id(call)
        OrderList.accept_order(data_set, user_id)
        await call.answer("Заказ отправлен!")
        await state.finish()
        await main_menu_handler(call.message)
    else:
        await call.answer("Заказ пуст!")


@dp.callback_query_handler(text_startswith=["remove_dish"], state=OrderUser.start_order)
@check_order_today
async def remove_dish_handler(call: CallbackQuery, state: FSMContext, *args, **kwargs):
    dish = call.data.split(":")[1]
    data = await state.get_data()
    data_set = data.get("data_set")
    data_set.remove(dish)
    await state.update_data(data_set=data_set)
    await call.message.edit_text(text=f"{dish} (убрано)")
    await call.answer("Список блюд обновлён")


@dp.callback_query_handler(text="to_main_menu", state=OrderUser.start_order)
async def menu_handler_back(call: CallbackQuery, *args, **kwargs):
    '''Back to the main menu'''
    await call.message.edit_reply_markup()
    await main_menu_handler(call.message)


@dp.callback_query_handler(text_startswith="dish", state=OrderUser.start_order)
@check_order_today
async def dish_handler(call: CallbackQuery, *args, **kwargs):
    '''Select dishes'''
    dish = call.data.split(':')[1]
    dishes = Dish.get_dishes(dish)
    await call.message.edit_text(text=hbold("ВЫБЕРИТЕ БЛЮДО"))
    for val in dishes:
        if val.dish_photo:
            with open(f"./photo/{val.dish_photo}", "rb") as photo:
                await call.message.answer_photo(photo=photo)
        await call.message.answer(text=f"Название: {val.dish_name}")
        await call.message.answer(text=f"Цена: {val.dish_price}р")
        await call.message.answer(
            text=f"Описание: {val.dish_description}",
            reply_markup=get_inline_keyboard_markup(
                text=f"Заказать {val.dish_name}",
                callback_data="add_dish:{0}".format(val.dish_name)
            )
        )
    await call.message.answer(
        text="Назад",
        reply_markup=get_inline_keyboard_markup(
            text="Назад",
            callback_data="to_menu"
        )
    )


@dp.callback_query_handler(text_startswith="add_dish", state=OrderUser.start_order)
@check_order_today
async def add_dish_handler(call: CallbackQuery, state: FSMContext, *args, **kwargs):
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