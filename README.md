# Сервисный центр - Веб-приложение

## Структура проекта

```
service-center/
├── app.py                  # Главный файл приложения
├── config.py               # Конфигурация
├── web_requirements.txt    # Зависимости
│
├── models/                 # Модели базы данных
│   ├── __init__.py
│   ├── user.py            # Модель пользователя
│   ├── client.py          # Модель клиента
│   ├── device.py          # Модель устройства
│   ├── order.py           # Модель заказа
│   └── part.py            # Модель запчасти
│
├── routes/                 # Маршруты приложения
│   ├── __init__.py
│   ├── auth.py            # Авторизация
│   ├── dashboard.py       # Панель управления
│   ├── clients.py         # Управление клиентами
│   ├── orders.py          # Управление заказами
│   └── parts.py           # Управление запчастями
│
├── templates/              # HTML шаблоны
│   ├── base.html
│   ├── welcome.html
│   ├── register_center.html
│   ├── login.html
│   ├── dashboard.html
│   ├── clients.html
│   ├── orders.html
│   └── parts.html
│
└── static/                 # Статические файлы
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Установка

```bash
pip install -r web_requirements.txt
```

## Запуск

```bash
python app.py
```

Приложение будет доступно по адресу: http://127.0.0.1:8080

## Вход по умолчанию

- **Логин:** admin
- **Пароль:** admin123

