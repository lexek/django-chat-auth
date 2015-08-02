# Установка
## прозрачно (через куки)
Будет работать только если чат и приложение на одном домене и приложение доступно через https.
* добавить `chat` в INSTALLED_APPS
* добавить `chat.ChatSessionAuthenticationMiddleware` в MIDDLEWARE_CLASSES после `AuthenticationMiddleware`
* добавить `chat.TransparentChatAuthenticationBackend` в AUTHENTICATION_BACKENDS
* задать CHAT_BASE (например `https://chathost:1337/`)

## имя и пароль
* добавить `chat` в INSTALLED_APPS
* добавить `chat.BasicChatBackend` в AUTHENTICATION_BACKENDS
* задать CHAT_BASE (например `https://chathost:1337/`)

# Зависимости
* django
* requests (http://requests.readthedocs.org/en/latest/)
