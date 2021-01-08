from aiogram.utils.markdown import hbold

from database.database import OrderList
from handlers.decorators import check_admin, check_authorization
from aiogram import types
from initialise import dp
from keyboards.inline_keyboard import admin_main_menu_keyboards, get_inline_keyboard_markup


@dp.callback_query_handler(text_startswith="admin_order_list")
async def admin_order_list(call: types.CallbackQuery):
    orders = OrderList.get_orders()
    if orders:
        await call.message.answer(text=hbold("ЗАКАЗЫ НА СЕГОДНЯ:"))
        for order in orders:
            await call.message.answer(text=f"Пользователь: {order.user_name}")
            await call.message.answer(text=f"Телефон: {order.user_phone_number}")
            await call.message.answer(
                text=f"Блюдо: {order.dish_name} {order.dish_price}р",
                reply_markup=get_inline_keyboard_markup(
                    text="Убрать заказ",
                    callback_data="drop_order"
                )
            )
    else:
        await call.answer("Заказы на сегодня ещё не поступили!")
        # pass
        # показ информации о заказе
        # [handler на [заказ выполнен]]

@dp.callback_query_handler(text_startswith="drop_order")
async def text_startswith_handler(call: types.CallbackQuery):
    pass



@dp.message_handler()
@check_authorization
@check_admin
async def admin_main_menu_handler(message: types.Message):
    await message.answer(
        text=hbold("ГЛАВНОЕ МЕНЮ АДМИНИСТРАТОРА"),
        reply_markup=admin_main_menu_keyboards
    )


# @dp.message_handler(content_types=['photo'])
# @check_autorization
# async def start_handler(message):
#     await message.photo[-1].download(f"photo/{message.photo[-1]['file_id']}.jpg")
#     await message.answer("Фото сохранено!")