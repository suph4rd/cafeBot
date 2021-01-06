from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.database import Category

menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Меню", callback_data="menu"),
            ],
            [
                InlineKeyboardButton(text="Изменить данные пользователя", callback_data="change_user"),
            ]
        ]
    )


category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мой заказ", callback_data="order_user")
        ],
        [InlineKeyboardButton(text=x.category_name, callback_data=f"dish:{x.category_name}")
         for x in Category.get_catygoryes()],
        [
            InlineKeyboardButton(text="Назад", callback_data="to_main_menu")
        ]
    ]
)

admin_main_menu_keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Меню на сегодня", callback_data="admin_menu"),
            ],
            [
                InlineKeyboardButton(text="Список заказов", callback_data="admin_order_list"),
            ],
            [
                InlineKeyboardButton(text="Работа с пользователями", callback_data="admin_change_user"),
            ]
        ]
    )