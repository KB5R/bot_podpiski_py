import toml
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = ""
CHAT_ID = ""
TOML_FILE = "subscriptions.toml"

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
    today = datetime.today().date() # Получаем дату без времени
    subscriptions = load_subscriptions() # Загрузка TOML

    if not subscriptions: # Если нет подписок то возврощаем "Нет активных подписок"
        logging.warning("Нет подписок для проверки.") 
        return "Нет активных подписок."

    all_subs = []       # Списки для подписок с датам конца
    expiring_soon = []  # Если меньше 30 дней пишем сюда

    for sub in subscriptions.values():
        try:
            name = sub["name"]
            expires = datetime.strptime(sub["expires"], "%Y-%m-%d").date()
            days_left = (expires - today).days

            all_subs.append(f"{name}: истекает {expires} ({days_left} дней)")

            if days_left <= 30:
                expiring_soon.append(f"⚠ {name}: {days_left} дней до окончания!")
        except Exception as e:
            logging.error(f"Ошибка обработки подписки {sub}: {e}")

    message = "📋 Все подписки:\n" + "\n".join(all_subs)
    if expiring_soon:
        message += "\n\n⏳ Скоро истекают:\n" + "\n".join(expiring_soon)
    
    return message



# Обработчик для отправки списка по кнопке /start
@dp.message(Command("start"))
async def send_subscriptions(message: Message):
    subscriptions_info = await check_subscriptions()
    await message.answer(subscriptions_info)



# Еще не протестировал
async def on_startup():
    """Запуск планировщика при старте бота."""
    scheduler.add_job(check_subscriptions, "cron", hour=10, minute=0)
    scheduler.start()
    logging.info("Планировщик запущен.")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    logging.info("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
