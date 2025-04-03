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
ADMIN_ID = os.getenv("ADMIN_ID")

print(ADMIN_ID)
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
            types.KeyboardButton(text="SSL"),
            types.KeyboardButton(text="Domain"),
            types.KeyboardButton(text="Средства защиты"),
            types.KeyboardButton(text="Другое")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите группу подписок"
    )
    if ADMIN_ID == str(message.from_user.id):
        await message.answer("Выберите группу подписок?", reply_markup=keyboard)
    else:
        await message.answer("Вы не прошли авторизацию")




# В subscriptions_info передаем выполнение check_subscriptions()
# Ну и выводми subscriptions_info
@dp.message(F.text.lower() == "другое")
async def send_subscriptions(message: Message):
    subscriptions_info = await check_subscriptions()
    await message.answer(subscriptions_info)



@dp.message(F.text.lower() == "ssl")
async def send_subscriptions_ssl(message: Message):
    subscriptions_info = await check_subscriptions_ssl()
    await message.answer(subscriptions_info)
# End keyboard ---------------------------------------------------

# Обработчики ----------------------------------------------------
# Обработчик /start находится в поле keyboard

@dp.message(Command("id"))
async def id_user(message: Message):
    message_user_id = message.from_user.id
    await message.answer(str(message_user_id))

#Other------------------------------------------------------------------

def load_subscriptions():
    """Загружает подписки из TOML-файла."""
    try:
        data = toml.load(TOML_FILE_OTHER)
        return data.get("other", {})
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

#Ens Other-------------------------------------------------------------------------------

# SSL ---------------------------------------------------------------------------------

def load_subscriptions_ssl():
    """Загружает подписки из TOML-файла."""
    try:
        data = toml.load(TOML_FILE_OTHER)
        return data.get("ssl", {})
    except Exception as e:
        logging.error(f"Ошибка загрузки TOML: {e}")
        return {}




async def check_subscriptions_ssl():
    today = datetime.today().date()      # Получаем дату без времени
    subscriptions = load_subscriptions_ssl() # Загрузка TOML

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



# END SSL -----------------------------------------------------------------------------





async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Бот запущен.")
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())