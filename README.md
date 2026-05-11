**Auth Service**

Auth Service предоставляет веб-API и Swagger по адресу http://0.0.0.0:8000/docs#/. В этом сервисе реализуются регистрация пользователя, вход (логин) и выдача JWT. Сервис хранит пользователей в базе (например SQLite или Postgres), хранит пароль только в виде хеша и формирует JWT с полями sub (id пользователя), role и временем жизни. Этот сервис является единственным местом, где выполняется “выпуск” токенов и управление пользователями.


**Bot Service**

Bot Service содержит Telegram-бота на aiogram. Основная логика: бот принимает сообщения пользователя, проверяет наличие JWT и валидирует его. Если токен валиден, бот отправляет запрос к LLM и возвращает ответ. Если токен отсутствует или неверный, бот отказывает в доступе и просит пользователя авторизоваться через Auth Service.

**Структура проекта**
```
llm_tg_bot/
├── auth_service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   ├── routes_auth.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── exceptions.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── users.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── user.py
│   │   └── usecases/
│   │       ├── __init__.py
│   │       └── auth.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth_api.py
│   │   └── test_security.py
│   ├── .env
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── uv.lock
│
├── bot_service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── bot/
│   │   │   ├── __init__.py
│   │   │   ├── dispatcher.py
│   │   │   └── handlers.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── jwt.py
│   │   ├── infra/
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   └── redis.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── openrouter_client.py
│   │   └── tasks/
│   │       ├── __init__.py
│   │       └── llm_tasks.py
│   ├── tests/
│   │  ├── __init__.py
│   │  ├── conftest.py
│   │  ├── test_handlers.py
│   │  ├── test_jwt_validation.py
│   │  └── test_openrouter.py
│   ├── __init__.py
│   ├── Dockerfile
│   ├── .env
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── uv.lock
├── screenshots
├── .gitignore
├── docker-compose.yml
├── main.py
└── README.md
```

**Сценарий работы**

1) Запуск приложения docker-compose up -d
2) Переход по ссылке: http://localhost:8000/docs и регистрация пользователя
3) Авторизация и получение токена 
4) Передача токена в ТГ бота @llm_py_bot командой /token 
5) Выполнение запросов к ИИ
6) Выключение докера sudo docker-compose down

**Сценарий тестирования**
1) Перейти в папку cd ~/final_python_llm/<Папка сервиса>
2) Синхронизировать виртуальное окружение uv: ```uv sync``` 
3) Провести тестирование ```uv run pytest tests/```



**Работа эндпоинтов в Swagger**

1) POST /auth/register 
![alt text](screenshots/register.png)

2) POST /auth/login
![alt text](screenshots/login.png)

3) GET /auth/me
![alt text](screenshots/get_me.png)

4) GET /health 
![alt text](screenshots/health.png)

**Telegram**

![alt text](screenshots/Пример_работы_бота.png)

**Rabbit**

1) Общий вид
![alt text](screenshots/RabbitMQ.png)

2) Демонстрация накопления сообщений
![alt text](screenshots/RabbitMQ_queued_messages.png)

**Тесты**

1) auth_service
![alt text](screenshots/Тестирование_auth_service.png)

2) bot_service 
![alt text](screenshots/Тестирование_bot_service.png)
