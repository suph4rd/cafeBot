from aiogram.utils.markdown import hbold
from database.database import OrderList, User
from handlers.decorators import check_admin, check_authorization
from aiogram import types
from initialise import dp
from keyboards.inline_keyboard import admin_main_menu_keyboards, get_inline_keyboard_markup, get_back, \
    get_admin_change_user_handler


@dp.callback_query_handler(text_startswith="admin_order_list")
async def admin_order_list(call: types.CallbackQuery, *args, **kwargs):
    orders = OrderList.get_orders()
    if orders:
        await call.message.answer(text=hbold("ЗАКАЗЫ НА СЕГОДНЯ:"))
        for order in orders:
            await call.message.answer(
                text=f"Пользователь: {hbold(order.user_name)}\n"
                     f"Телефон: {order.user_phone_number}\n"
                     f"Блюдо: {order.dish_name} {order.dish_price}р",
                reply_markup=get_inline_keyboard_markup(
                    text="Убрать заказ",
                    callback_data=f"drop_order:{order.user_id}:{order.dish_name}"
                )
            )
        await get_back(call, callback_data="to_admin_main_menu")
    else:
        await call.answer("Заказы на сегодня ещё не поступили!")


@dp.callback_query_handler(text_startswith="drop_order")
async def drop_order_handler(call: types.CallbackQuery, *args, **kwargs):
    user_id = call.data.split(":")[1]
    dish_name = call.data.split(":")[2]
    OrderList.drop_order(user_id, dish_name)
    await call.message.edit_text(text=hbold(f"Блюдо {dish_name} убрано"))


@dp.callback_query_handler(text_startswith="admin_change_user_edit")
async def admin_change_user_edit_handler(call: types.CallbackQuery, *args, **kwargs):
    from states.states import Registration
    await Registration.not_registration.set()
    from handlers import autorization
    user_id = call.data.split(":")[1]
    await autorization.registration_not_registration_handler(call.message, user_id=user_id)


@dp.callback_query_handler(text_startswith="admin_change_user_is_active")
async def admin_change_user_is_active_handler(call: types.CallbackQuery, *args, **kwargs):
    user_id = int(call.data.split(":")[1])
    is_active = call.data.split(":")[2]
    is_active = True if is_active == "False" else False
    change = User.update_user({
        "is_active": is_active,
        "user_id": user_id
    })
    if change:
        await call.message.edit_reply_markup(reply_markup=get_admin_change_user_handler(
            user_id,
            status=is_active))
        await call.answer("Изменения приняты!")


@dp.callback_query_handler(text_startswith="admin_change_user")
async def admin_change_user_handler(call: types.CallbackQuery, *args, **kwargs):
    await call.message.answer("Пожалуйста подождите, идёт загрузка пользователей!")
    users = User.get_users()
    await call.message.answer(text=hbold("СПИСОК ПОЛЛЬЗОВАТЕЛЕЙ:"))
    for num, user in enumerate(users, start=1):
        await call.message.answer(
            text=f"{num}.Пользователь: {hbold(user.fio)}\n"
                 f"Телефон: {user.phone_number}\n"
                 f"ID: {user.user_id}",
            reply_markup=get_admin_change_user_handler(user.user_id)
        )
    await get_back(call, callback_data="to_admin_main_menu")


@dp.message_handler()
@check_authorization
@check_admin
async def admin_main_menu_handler(message: types.Message, *args, **kwargs):
    await message.answer(
        text=hbold("ГЛАВНОЕ МЕНЮ АДМИНИСТРАТОРА"),
        reply_markup=admin_main_menu_keyboards
    )


@dp.callback_query_handler(text="to_admin_main_menu")
async def admin_main_menu_handler_back(call: types.CallbackQuery, *args, **kwargs):
    await admin_main_menu_handler(call.message)

# @dp.message_handler(content_types=['photo'])
# @check_autorization
# async def start_handler(message):
#     await message.photo[-1].download(f"photo/{message.photo[-1]['file_id']}.jpg")
#     await message.answer("Фото сохранено!")
