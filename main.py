import toml
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv
import os

load_dotenv() # Загрузка .env


TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TOML_FILE = os.getenv("TOML_FILE")

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()




def load_subscriptions():
    """Загружает подписки из TOML-файла."""
    try:
        data = toml.load(TOML_FILE)
        return data.get("subscriptions", {})
    except Exception as e:
        logging.error(f"Ошибка загрузки TOML: {e}")
        return {}




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




# Обработчик для отправки списка по кнопке /start
@dp.message(Command("start"))
async def send_subscriptions(message: Message):
    subscriptions_info = await check_subscriptions()
    await message.answer(subscriptions_info)




async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Бот запущен.")
    await dp.start_polling(bot)

#-----------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
