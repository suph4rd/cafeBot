from aiogram.utils.markdown import hbold
from handlers.decorators import check_admin, check_authorization
from aiogram import types
from initialise import dp
from keyboards.inline_keyboard import admin_main_menu_keyboards



@dp.callback_query_handler(text_startswith="admin_order_list")
async def admin_order_list(message: types.Message):
    orders = "Запрос на заказы"
    for order in orders:
        pass
        # показ информации о заказе
        # [handler на [заказ выполнен]]

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