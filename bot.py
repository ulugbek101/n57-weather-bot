from asyncio import run
from logging import basicConfig, INFO

from aiogram.filters.command import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher
from aiogram import F

from weather_data import get_weather_data
from keyboards import generate_save_city_menu, generate_cities_menu
from database import db

TOKEN = "7880642169:AAEhs-Zi8niuXatZ4q8ng6KMPaxfEVFHc5Q"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    try:
        db.register_user(telegram_id, username, fullname)
        await message.answer(text="<b>Siz muvaffaqiyatli ro'yxatga olindingiz</b>",
                            parse_mode="HTML")
    except:
        await message.answer(text="<b>Xush kelibsiz !</b>", parse_mode="HTML")


@dp.message()
async def answer_weather_data(message: Message):
    city_name = message.text

    data = get_weather_data(city_name=city_name)

    if data:
        await message.answer(text=data, parse_mode="HTML", reply_markup=generate_save_city_menu(city_name=city_name))
    else:
        await message.answer(text="<b>Bunday shahar mavjud emas</b>",
                             parse_mode="HTML")



@dp.callback_query()
async def save_city(call: CallbackQuery):
    city_name = call.data.split(":")[-1]
    telegram_id = call.from_user.id

    try:
        db.register_city(telegram_id, city_name)
        await call.message.answer(text="Shahar saqlandi", reply_markup=generate_cities_menu(telegram_id=call.from_user.id))
    except:
        await call.answer(text="Shahar allaqachon saqlangan", show_alert=True)


async def main():
    # basicConfig(level=INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())
