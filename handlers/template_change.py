from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold
from database.database import Template, Category, Dish
from initialise import dp
from keyboards.inline_keyboard_template import get_template_keyboard, template_change_keyboard, \
    get_template_category_keyboard, get_template_category_dishes_keyboard, dish_keyboard
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
    template_id = call.data.split(":")[2]
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


@dp.callback_query_handler(text="add_new_template_category", state=[ChangeTemplate])
async def template_edit_add_category_handler(call: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    await ChangeTemplate.add_category.set()
    await call.message.edit_text(
        text=hbold(f"Введите название категории"),
    )


@dp.callback_query_handler(text="template_edit_category_add_select_delete", state=ChangeTemplate)
async def template_edit_category_add_select_delete_handler(call: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    data = await state.get_data()
    dish_id = data.get("dish_id")
    Dish.drop_dish(dish_id)
    data.pop("dish_name")
    data.pop("dish_describe")
    data.pop("dish_price")
    data.pop("dish_photo")
    data.pop("dish_id")
    await state.update_data(data=data)
    await template_edit_category_handler(call, state)


@dp.callback_query_handler(text_startswith="template_edit_category_add_select", state=ChangeTemplate)
async def template_edit_category_add_select_handler(call: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    dish_name = call.data.split(":")[1]
    dish_id = call.data.split(":")[2]
    dish_query = Dish.get_dish(dish_id)
    await state.update_data({
        "dish_id": dish_query.id,
        "dish_name": dish_query.dish_name,
        "dish_description": dish_query.dish_description,
        "dish_price": dish_query.dish_price,
        "dish_photo": dish_query.dish_photo
    })
    await call.message.edit_text(
        text=hbold(f"Работа с блюдом {dish_name}"),
        reply_markup=dish_keyboard
        )


@dp.callback_query_handler(text="template_edit_category_delete", state=ChangeTemplate)
async def template_edit_category_delete_handler(call: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    category_id = (await state.get_data("category_id")).get("category_id")
    category_name = (await state.get_data("category_name")).get("category_name")
    Category.drop_category(category_id)
    await call.answer(f"Шаблон {category_name} удалён!")
    await ChangeTemplate.start.set()
    await admin_menu_template_change_handler(call, state)


@dp.message_handler(state=[ChangeTemplate.dish_name])
async def template_edit_category_add_describe_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    await ChangeTemplate.dish_describe.set()
    dish_name = message.text
    await state.update_data({"dish_name": dish_name})
    dish_describe = (await state.get_data("dish_describe")).get("dish_describe")
    if dish_describe:
        await message.answer(hbold(f"Описание блюда (текущее:{dish_describe})"))
    else:
        await message.answer(hbold("Описание блюда"))


@dp.message_handler(state=[ChangeTemplate.dish_describe])
async def template_edit_category_add_price_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    await ChangeTemplate.dish_price.set()
    dish_describe = message.text
    await state.update_data({"dish_describe": dish_describe})
    dish_price = (await state.get_data("dish_price")).get("dish_price")
    if dish_price:
        await message.answer(hbold(f"Введите цену блюда (текущая:{dish_price})"))
    else:
        await message.answer(hbold("Введите цену блюда"))


@dp.message_handler(state=[ChangeTemplate.dish_price])
async def template_edit_category_add_photo_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    await ChangeTemplate.dish_photo.set()
    dish_price = message.text
    await state.update_data({"dish_price": dish_price})
    await message.answer(hbold("Отправте фото"))


@dp.message_handler(content_types='photo', state=[ChangeTemplate.dish_photo])
async def template_edit_category_save_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    await ChangeTemplate.category_edit.set()
    data = await state.get_data()
    data["dish_photo"] = f"photo/{data.get('dish_name')}.jpg"
    print(data.get("dish_photo"))
    await message.photo[-1].download(data.get("dish_photo"))
    Dish.add_or_update_dish(data)
    data.pop("dish_name")
    data.pop("dish_describe")
    data.pop("dish_price")
    data.pop("dish_photo")
    if data.get("dish_id"):
        data.pop("dish_id")
    await state.update_data(data=data)
    await template_edit_category_handler(message, state)


@dp.callback_query_handler(text_startswith="template_edit_category_dish_add", state=[ChangeTemplate])
async def template_edit_category_dish_add_handler(call: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    await ChangeTemplate.dish_name.set()
    dish_name = (await state.get_data("dish_name")).get("dish_name")
    if dish_name:
        await call.message.edit_text(hbold(f"Введите название блюда (текущее:{dish_name})"))
    else:
        await call.message.edit_text(hbold(f"Введите название блюда"))


@dp.message_handler(state=[ChangeTemplate])
@dp.callback_query_handler(text_startswith="template_edit_category", state=[ChangeTemplate])
async def template_edit_category_handler(message, state: FSMContext, *args, **kwargs):
    await ChangeTemplate.category_edit.set()
    if isinstance(message, types.CallbackQuery):
        if len(message.data.split(":")) == 3:
            category_name = message.data.split(":")[1]
            category_id = message.data.split(":")[2]
            await state.update_data({
                "category_name": category_name,
                "category_id": category_id
            })
        else:
            category_name = (await state.get_data("category_name")).get("category_name")
            category_id = (await state.get_data("category_id")).get("category_id")
        await message.message.edit_text(
            text=hbold(f"Редактирование категории {category_name}"),
            reply_markup=get_template_category_dishes_keyboard(category_name, category_id)
        )
    else:
        category_name = (await state.get_data("category_name")).get("category_name")
        category_id = (await state.get_data("category_id")).get("category_id")
        await message.answer(
            text=hbold(f"Редактирование категории {category_name}"),
            reply_markup=get_template_category_dishes_keyboard(category_name, category_id)
        )


@dp.message_handler(state=ChangeTemplate.add_template)
async def add_new_template_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    template_name = message.text
    Template.create_template(template_name)
    template_id = Template.get_template_id(template_name)
    await state.set_data({
        "template_name": template_name,
        "template_id": template_id
    })
    await ChangeTemplate.start.set()
    await admin_menu_template_change_handler(message, state)


@dp.message_handler(state=[ChangeTemplate])
@dp.callback_query_handler(text="admin_menu_template_change", state=[ChangeTemplate])
async def admin_menu_template_change_handler(message, state: FSMContext, *args, **kwargs):
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
