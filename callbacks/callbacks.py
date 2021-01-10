from aiogram.utils.callback_data import CallbackData


dish_callback = CallbackData("dish", "category")
add_dish_callback = CallbackData("add_dish", "dish")
remove_dish_callback = CallbackData("remove_dish", "dish")
drop_order_callback = CallbackData("drop_order", "user_id", "dish_name")
admin_change_user_is_active_callback = CallbackData("admin_change_user_is_active", "user_id", "is_active")
admin_change_user_edit_callback = CallbackData("admin_change_user_edit", "user_id")
text_startswith_callback = CallbackData("text_startswith", "template_name")