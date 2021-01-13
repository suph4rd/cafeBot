from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.database import Template, Category, Dish

template_change_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Редактировать шаблон", callback_data="admin_menu_template_change")],
        [InlineKeyboardButton(text="Удалить шаблон", callback_data="admin_menu_template_delete")],
        [InlineKeyboardButton(text="Назад", callback_data="to_template_change")]
    ]
)


def get_template_keyboard():
    """:return: Keyboard with loop of template buttons"""
    button_list = [[InlineKeyboardButton(text="Добавить новый шаблон", callback_data="add_new_template")]]
    button_list_pref = [[InlineKeyboardButton(
        text=x.template_name,
        callback_data=f"select_template:{x.template_name}:{x.id}"
    )]
        for x in Template.get_templates()]

    button_list += button_list_pref
    button_list.append([InlineKeyboardButton(text="Назад", callback_data="admin_menu_status")])

    category_keyboard = InlineKeyboardMarkup(
        inline_keyboard=button_list
    )
    return category_keyboard


def get_template_category_keyboard(template_name, template_id):
    """:return: Keyboard with loop of category buttons for edit template category"""
    button_list = [[InlineKeyboardButton(text="Добавить новую категорию", callback_data="add_new_template_category")]]
    button_list_pref = [[InlineKeyboardButton(
        text=x.category_name,
        callback_data=f"template_edit_category:{x.category_name}:{x.id}"
    )]
        for x in Category.get_catygoryes(template_id)]

    button_list += button_list_pref                                                         # mb + template_id???
    button_list.append([InlineKeyboardButton(text="Назад", callback_data=f"select_template:{template_name}:{template_id}")])

    category_keyboard = InlineKeyboardMarkup(
        inline_keyboard=button_list
    )
    return category_keyboard


def get_template_category_dishes_keyboard(category_name, category_id):
    """
    :return: Keyboard with loop of category buttons for edit template category
    """
    button_list = [
        [InlineKeyboardButton(text=f"Удалить {category_name}", callback_data="template_edit_category_delete")],
        [InlineKeyboardButton(text="Добавить новое блюдо", callback_data="template_edit_category_dish_add")]
    ]
    button_list_pref = [[InlineKeyboardButton(
        text=x.dish_name,
        callback_data=f"template_edit_category:{x.dish_name}:{x.id}"
    )]
        for x in Dish.get_dishes_category(category_id)]  # Dish!!!!!!!!!!

    button_list += button_list_pref
    button_list.append([InlineKeyboardButton(text="Назад", callback_data="admin_menu_template_change")])

    category_keyboard = InlineKeyboardMarkup(
        inline_keyboard=button_list
    )
    return category_keyboard
