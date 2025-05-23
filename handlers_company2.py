import asyncio
import toml
from dotenv import load_dotenv
import os
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import  F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from datetime import datetime
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
load_dotenv() # Загрузка .env


TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TOML_FILE_OTHER = os.getenv("TOML_FILE_OTHER")
ADMIN_ID = os.getenv("ADMIN_ID")

route2 = Router()




@route2.message(F.text.lower() == "company2")
async def cmd_sub_company_1(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="SSL_I"),
            types.KeyboardButton(text="Domain_I")
        ],
        [
            types.KeyboardButton(text="DNS_I"),
            types.KeyboardButton(text="Другое_I")
        ],
        [
            types.KeyboardButton(text="Все подписки_I")
        ],
        [
            types.KeyboardButton(text="Назад")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите группу подписок"
    )
    if str(message.from_user.id) in ADMIN_ID:
        await message.answer("Выберите группу подписок", reply_markup=keyboard)
    else:
        await message.answer("Вы не прошли авторизацию")




# Обработчики ----------------------------------------------------
# Обработчик /start находится в поле keyboard

# В subscriptions_info передаем выполнение check_subscriptions()
# Ну и выводми subscriptions_info
# Other
@route2.message(F.text.lower() == "назад")
async def send_subscriptions(message: Message):
    if str(message.from_user.id) in ADMIN_ID:
        await message.answer("Выберите группу подписок",cmd_sub_company_1)



@route2.message(F.text.lower() == "другое_i")
async def send_subscriptions(message: Message):
    subscriptions_info = check_subscriptions_other()
    if str(message.from_user.id) in ADMIN_ID:
        await message.answer(subscriptions_info)


# Добавил авторизацию 
# SSL
@route2.message(F.text.lower() == "ssl_i")
async def send_subscriptions_ssl(message: Message):
    subscriptions_info = check_subscriptions_ssl()
    if str(message.from_user.id) in ADMIN_ID:
        await message.answer(subscriptions_info)

# DOMAIN
@route2.message(F.text.lower() == "domain_i")
async def send_subscriptions_domain(message: Message):
    subscriptions_info = check_subscriptions_domain()
    if str(message.from_user.id) in ADMIN_ID:
        await message.answer(subscriptions_info)

# FIREWALL
@route2.message(F.text.lower() == "dns_i")
async def send_subscriptions_firewall(message: Message):
    subscriptions_info = check_subscriptions_firewall()
    if str(message.from_user.id) in ADMIN_ID:
        await message.answer(subscriptions_info)


# ALL

@route2.message(F.text.lower() == "все подписки_i")
async def send_all_subscriptions(message: Message):
    message_user_id = message.from_user.id
    if str(message_user_id) in ADMIN_ID:
        # Получаю все подписки
        subscriptions_info_other = check_subscriptions_other()
        subscriptions_info_ssl = check_subscriptions_ssl()
        subscriptions_info_domain = check_subscriptions_domain()
        subscriptions_info_firewall = check_subscriptions_firewall()
        # В одно сообщение
        all_subscriptions_info = (
            f"\n{subscriptions_info_other}\n\n"
            f"\n{subscriptions_info_ssl}\n\n"
            f"\n{subscriptions_info_domain}\n\n"
            f"\n{subscriptions_info_firewall}\n\n"
        )
        
        await message.answer(all_subscriptions_info)

# End обработчики -----------------------------------------------------


#Other------------------------------------------------------------------

def load_subscriptions():
    """Загружает подписки из TOML-файла."""
    try:
        data = toml.load(TOML_FILE_OTHER)
        return data.get("other_i", {})
    except Exception as e:
        logging.error(f"Ошибка загрузки TOML: {e}")
        return {}




def check_subscriptions_other():
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


    message_parts = ["📋 Все другие подписки:"] + all_subs

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
        return data.get("ssl_i", {})
    except Exception as e:
        logging.error(f"Ошибка загрузки TOML: {e}")
        return {}




def check_subscriptions_ssl():
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


    message_parts = ["📋 Все SSL:"] + all_subs

    if expiring_soon:
        message_parts.append("\n⏳ Скоро истекают:")
        message_parts.extend(expiring_soon)

    return "\n".join(message_parts)



# END SSL -----------------------------------------------------------------------------


# Domain ------------------------------------------------------------------------------

def load_subscriptions_domain():
    try:
        data = toml.load(TOML_FILE_OTHER)
        return data.get("domain_i", {})
    except Exception as e:
        logging.error(f"Ошибка загрузки TOML: {e}")
        return {}




def check_subscriptions_domain():
    today = datetime.today().date()      # Получаем дату без времени
    subscriptions = load_subscriptions_domain() # Загрузка TOML

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


    message_parts = ["📋 Все Domain:"] + all_subs

    if expiring_soon:
        message_parts.append("\n⏳ Скоро истекают:")
        message_parts.extend(expiring_soon)

    return "\n".join(message_parts)

# END Domain---------------------------------------------------------------------------

# FIREWALL ---------------------------------------------------------------------

def load_subscriptions_firewall():
    try:
        data = toml.load(TOML_FILE_OTHER)
        return data.get("dns_i", {})
    except Exception as e:
        logging.error(f"Ошибка загрузки TOML: {e}")
        return {}




def check_subscriptions_firewall():
    today = datetime.today().date()      # Получаем дату без времени
    subscriptions = load_subscriptions_firewall() # Загрузка TOML

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


    message_parts = ["📋 Все :"] + all_subs

    if expiring_soon:
        message_parts.append("\n⏳ Скоро истекают:")
        message_parts.extend(expiring_soon)

    return "\n".join(message_parts)


# END FIREWALL -----------------------------------------------------------------