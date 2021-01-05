from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.database import Category, Dish

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


# def get_dish(category):
#     dishes_keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text=x.dish_name, callback_data=f"add_dish:{x.dish_name}")
#              for x in Dish.get_dishes(category)],
#             [
#                 InlineKeyboardButton(text="Назад", callback_data="to_menu")
#             ]
#         ]
#     )
#     return dishes_keyboard