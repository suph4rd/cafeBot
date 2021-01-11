from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from database.database import Template, Category
from initialise import dp, bot
from keyboards.inline_keyboard_template import get_template_keyboard, template_change_keyboard, \
    get_template_category_keyboard
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
    template_id = Template.get_template_id(template_name)
    await ChangeTemplate.start.set()
    state = dp.current_state()
    await state.set_data({
        "template_name": template_name,
        "template_id": template_id
    })
    await call.message.edit_text(
        text=hbold(f"Работа с шаблоном {template_name}"),
        reply_markup=template_change_keyboard
    )


@dp.message_handler(state=[ChangeTemplate.add_category])
async def template_edit_add_category_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    category_name = message.text
    template_id = (await state.get_data("template_id")).get("template_id")
    Category.add_category(category_name, template_id)
    await ChangeTemplate.start.set()
    await admin_menu_template_change_handler(message, state)


@dp.callback_query_handler(text="admin_menu_template_delete", state=[ChangeTemplate])
async def admin_menu_template_delete_handler(call: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    template_id = (await state.get_data("template_id")).get("template_id")
    template_name = (await state.get_data("template_name")).get("template_name")
    Template.drop_template(template_id)
    if state:
        await state.finish()
    await call.answer(text=f"Шаблон {template_name} удалён!")
    await select_menu_today_handler(call)


@dp.callback_query_handler(text="add_new_template")
async def add_new_template_handler(call: types.CallbackQuery, *args, **kwargs):
    await ChangeTemplate.add_template.set()
    await call.message.edit_text(hbold("Введите название шаблона!"))


@dp.message_handler(state=ChangeTemplate.add_template)
async def add_new_template_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    template_name = message.text
    print(template_name)
    Template.create_template(template_name)
    template_id = Template.get_template_id(template_name)
    await state.set_data({
        "template_name": template_name,
        "template_id": template_id
    })
    await ChangeTemplate.start.set()
    await admin_menu_template_change_handler(message, state)
    # Редирект на редактирование шаблона со сменой состояния


@dp.message_handler(state=[ChangeTemplate])
@dp.callback_query_handler(text="admin_menu_template_change", state=[ChangeTemplate])
async def admin_menu_template_change_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    template_name = (await state.get_data("template_name")).get("template_name")
    template_id = (await state.get_data("template_id")).get("template_id")
    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(
            text=hbold(f"Редактирование шаблона {template_name}"),
            reply_markup=get_template_category_keyboard(template_name, template_id)
        )
    else:
        await message.answer(
            text=hbold(f"Редактирование шаблона {template_name}"),
            reply_markup=get_template_category_keyboard(template_name, template_id)
        )


@dp.callback_query_handler(text="add_new_template_category", state=[ChangeTemplate])
async def template_edit_add_category_handler(call: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    await ChangeTemplate.add_category.set()
    await call.message.edit_text(
        text=hbold(f"Введите название категории"),
    )












# add_new_template
