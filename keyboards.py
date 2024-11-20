from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database import db


def generate_save_city_menu(city_name: str):
    markup = InlineKeyboardBuilder()
    markup.button(text="Shaharni saqlash", callback_data=f"save_city:{city_name}")
    return markup.as_markup()



def generate_cities_menu(telegram_id: int):
    user = db.get_user(telegram_id)
    cities = db.get_cities(user.get("id"))  # ["Toshkent", "Samarqand", ...]

    markup = ReplyKeyboardBuilder()

    for city_object in cities:
        markup.button(text=city_object.get("name"))
    
    markup.adjust(2)
    return markup.as_markup(resize_keyboard=True)
