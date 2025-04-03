# Telegram Bot for tracking subscriptions

## Quick start

```
pip install -r requirements.txt
```

### Example of .env
```
TOKEN = "123456789:ABCD-123123123"
CHAT_ID = "12345678"
ADMIN_ID = {"1234123","00120001"}
TOML_FILE = "./subscriptions.toml"
```


### Example of subscriptions.toml

```toml
[subscriptions]
apple_developer = { name = "Apple Developer Program", expires = "2026-02-23" }
netflix = { name = "Netflix", expires = "2025-04-10" }
spotify = { name = "Spotify", expires = "2025-05-02" }
```

### Get to /start
```
📋 Все подписки:
Apple Developer Program: истекает 2026-02-23 (327 дней)
Netflix: истекает 2025-04-10 (8 дней)
Spotify: истекает 2025-05-02 (30 дней)

⏳ Скоро истекают:
⚠️ Netflix: 8 дней до окончания!
⚠️ Spotify: 30 дней до окончания!
```

### Авторизация 

```python
    if if ADMIN_ID == str(message.from_user.id):
        await message.answer("Выберите группу подписок?", reply_markup=keyboard)
    else:
        await message.answer("Вы не прошли авторизацию")
```
**Вот такой способ подходит если ADMIN_ID хранит только одно id**
**Пример**
```
ADMIN_ID = "123456"
```
**Но если хотим что бы у нас было несколько ADMIN_ID и все работало используйте**
```python
    if str(message.from_user.id) in ADMIN_ID:
        await message.answer("Выберите группу подписок?", reply_markup=keyboard)
    else:
        await message.answer("Вы не прошли авторизацию")
```
```
ADMIN_ID = {"123123","311231"}
```

## Quick start docker

**1. Clone**
```
git clone https://github.com/KB5R/bot_podpiski_py.git
```

**2. Example of .env**
```
TOKEN = "123456789:ABCD-123123123"
CHAT_ID = "12345678"
ADMIN_ID = {"1234123","00120001"}
TOML_FILE = "./subscriptions.toml"
```


**3. Example of subscriptions.toml**

```toml
[subscriptions]
apple_developer = { name = "Apple Developer Program", expires = "2026-02-23" }
netflix = { name = "Netflix", expires = "2025-04-10" }
spotify = { name = "Spotify", expires = "2025-05-02" }
```

**4. Build docker container**

```
docker build -t bot-podpisky-py .
```

```
docker images

REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
bot-podpisky-py   latest    e5ab1c12be15   16 minutes ago   156MB
```
**5.Run docker container**

```
docker run -d bot-podpisky-py
```