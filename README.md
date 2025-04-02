# Telegram Bot for tracking subscriptions

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
