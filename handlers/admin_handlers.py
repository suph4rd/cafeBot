from aiogram import types
import handlers.decorators as dec
from initialise import dp


@dp.message_handler()
@dec.check_admin
async def admin_main_menu_handler(message: types.Message):
    await message.answer(text="ГЛАВНОЕ МЕНЮ АДМИНИСТРАТОРА")


# @dp.message_handler(content_types=['photo'])
# @check_autorization
# async def start_handler(message):
#     await message.photo[-1].download(f"photo/{message.photo[-1]['file_id']}.jpg")
#     await message.answer("Фото сохранено!")