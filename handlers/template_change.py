from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from initialise import dp
from keyboards.inline_keyboard_template import get_template_keyboard, template_change_keyboard
from states.states import ChangeTemplate


@dp.callback_query_handler(text="template_change")
async def select_menu_today_handler(call: types.CallbackQuery, *args, **kwargs):
    await call.message.edit_text(
        text=hbold("Работа с шаблонами"),
        reply_markup=get_template_keyboard()
    )


@dp.callback_query_handler(text="to_template_change", state=[None, ChangeTemplate])
async def to_template_change_handler(call: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    if state:
        await state.finish()
    await select_menu_today_handler(call)


@dp.callback_query_handler(text_startswith="select_template", state=[None, ChangeTemplate])
async def select_template_handler(call: types.CallbackQuery, *args, **kwargs):
    template_name = call.data.split(":")[1]
    await ChangeTemplate.start.set()
    state = dp.current_state()
    await state.set_data({"template_name": template_name})
    await call.message.edit_text(
        text=hbold(f"Работа с шаблоном {template_name}"),
        reply_markup=template_change_keyboard
    )

# add_new_template
