import toml
import os
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F

from handlers_company1 import route

from dotenv import load_dotenv
import os

load_dotenv() # Загрузка .env


TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TOML_FILE_OTHER = os.getenv("TOML_FILE_OTHER")
ADMIN_ID = os.getenv("ADMIN_ID")

COMPANY1 = os.getenv("COMPANY1")
COMPANY2 = os.getenv("COMPANY2")
COMPANY3 = os.getenv("COMPANY3")
COMPANY4 = os.getenv("COMPANY4")

print(ADMIN_ID)
print(os.path.abspath(TOML_FILE_OTHER))


bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Keyboard -------------------------------------------------------
# https://mastergroosha.github.io/aiogram-3-guide/buttons/  Ru Tutor

@dp.message(Command("start"))
async def cmd_sub_company(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="COMPANY1"),
            types.KeyboardButton(text="COMPANY2")
        ],
        [
            types.KeyboardButton(text="COMPANY3"),
            types.KeyboardButton(text="COMPANY4")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите компанию"
    )
    if str(message.from_user.id) in ADMIN_ID:
        await message.answer("Выберите компанию", reply_markup=keyboard)
    else:
        await message.answer("Вы не прошли авторизацию")


# End keyboard ---------------------------------------------------
# Connect Company-------------------------------------------------
@dp.message(F.text.lower() == "company")
async def id_user(message: Message):
    await message.answer("Вы выбрали СOMPANY1")

# END Con Company

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Бот запущен.")
    dp.include_router(route)
    await dp.start_polling(bot)

@dp.message(F.text.lower() == "назад")
async def id_user(message: Message):
    await cmd_sub_company(message)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())