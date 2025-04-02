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



from dotenv import load_dotenv
import os

load_dotenv() # Загрузка .env


TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TOML_FILE_OTHER = os.getenv("TOML_FILE_OTHER")

print(os.path.abspath(TOML_FILE_OTHER))


bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Keyboard -------------------------------------------------------
# https://mastergroosha.github.io/aiogram-3-guide/buttons/

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="SSL & Domain"),
            types.KeyboardButton(text="Другое")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите группу подписок"
    )
    await message.answer("Выберите группу подписок?", reply_markup=keyboard)


# В subscriptions_info передаем выполнение check_subscriptions()
# Ну и выводми subscriptions_info
@dp.message(F.text.lower() == "другое")
async def send_subscriptions(message: Message):
    subscriptions_info = await check_subscriptions()
    await message.answer(subscriptions_info)


# End keyboard ---------------------------------------------------



# TOML Config ----------------------------------------------------
# TOML для типа "Другое"
def load_subscriptions():
    """Загружает подписки из TOML-файла."""
    try:
        data = toml.load(TOML_FILE_OTHER)
        return data.get("subscriptions", {})
    except Exception as e:
        logging.error(f"Ошибка загрузки TOML: {e}")
        return {}




# Toml end ------------------------------------------------------



async def check_subscriptions():
    today = datetime.today().date()      # Получаем дату без времени
    subscriptions = load_subscriptions() # Загрузка TOML

    if not subscriptions:                # Если нет подписок
        return "Нет активных подписок."

    all_subs = []       # Списки для подписок с датам конца
    expiring_soon = []  # Если меньше 30 дней пишем сюда

    # expires - дата окончания подписки
    # today   - текущая дата



    for sub in subscriptions.values():

        name = sub["name"]
        expires = datetime.strptime(sub["expires"], "%Y-%m-%d").date()
        days_left = (expires - today).days                                 # expires - today — разница между датами и .days получаем дни из timedelta

        all_subs.append(f"{name}: истекает {expires} ({days_left} дней)")  # .append() = добавления элемента в конец списка

        if days_left <= 30: # Если <= 30 то сохроняем в expiring_soon
            expiring_soon.append(f"⚠ {name}: {days_left} дней до окончания!")


    message_parts = ["📋 Все подписки:"] + all_subs

    if expiring_soon:
        message_parts.append("\n⏳ Скоро истекают:")
        message_parts.extend(expiring_soon)

    return "\n".join(message_parts)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Бот запущен.")
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())