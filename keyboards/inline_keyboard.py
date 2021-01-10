from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold

from database.database import Category, User

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
        [InlineKeyboardButton(text="Меню на сегодня", callback_data="admin_menu_status")],
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


async def get_back(call: types.CallbackQuery, callback_data):
    await call.message.answer(
        text=hbold("Назад"),
        reply_markup=get_inline_keyboard_markup(
            text="Назад",
            callback_data=callback_data
        )
    )


def get_admin_change_user_handler(user_id, status=None):
    if not isinstance(status, bool):
        status = User.check_user_is_active(user_id)
    status_name = "неактивным" if status else "активным"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Редактировать", callback_data=f"admin_change_user_edit:{user_id}")],
            [InlineKeyboardButton(
                text=f"Сделать {status_name}",
                callback_data=f"admin_change_user_is_active:{user_id}:{status}"
            )],
        ]
    )
    return keyboard


keyboard_admin_menu_status = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбор меню на сегодня", callback_data="select_menu_today")],
        [InlineKeyboardButton(text="Сделать меню неактивным", callback_data="menu_today_false")],
        [InlineKeyboardButton(text="Работа с шаблонами", callback_data="template_change")],
        [InlineKeyboardButton(text="Назад", callback_data="to_admin_main_menu")]
    ]
)
