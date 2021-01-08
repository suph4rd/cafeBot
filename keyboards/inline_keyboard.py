from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import Category


menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Меню", callback_data="menu")],
            [InlineKeyboardButton(text="Изменить данные пользователя",
                                  callback_data="change_user")]
        ]
    )


def get_category_keyboard():
    '''
    :return: keyboard with loop of category buttons
    '''
    button_list = [[InlineKeyboardButton(text="Мой заказ", callback_data="order_user")]]
    button_list_pref = [[InlineKeyboardButton(
        text=x.category_name,
        callback_data=f"dish:{x.category_name}"
    )]
    for x in Category.get_catygoryes()]

    button_list += button_list_pref
    button_list.append([InlineKeyboardButton(text="Назад", callback_data="to_main_menu")])

    category_keyboard = InlineKeyboardMarkup(
        inline_keyboard=button_list
    )
    return category_keyboard


admin_main_menu_keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Меню на сегодня", callback_data="admin_menu")],
            [InlineKeyboardButton(text="Список заказов", callback_data="admin_order_list")],
            [InlineKeyboardButton(text="Работа с пользователями", callback_data="admin_change_user")]
        ]
    )


def get_inline_keyboard_markup(text, callback_data):
    '''
    :param text: text in button
    :param callback_data: callback function for treatment button
    :return: keyboard with 1 button for loop
    '''
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text=text,
        callback_data=callback_data
    )]])
    return keyboard
