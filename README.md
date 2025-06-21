# 🔐 Мультивалютный Криптокошелек - Telegram Bot
**Выпускная квалификационная работа**  
**Студент:** Першин Никита Геннадьевич  

![Python Version](https://img.shields.io/badge/python-3.9.6-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📌 О проекте
Telegram-бот для демонстрации работы с криптовалютным мультикошельками, включая:
- Генерацию кошельков
- Шифрованное хранение приватных ключей
- Просмотр баланса
- Переводы

> ⚠️ **Важно!** Это учебный проект. Не используйте для реальных криптовалютных операций!

## 🛠 Установка

### Требования
- Python 3.9.6
- PostgreSQL 15+
- PgAdmin 4 (рекомендуется)
- установите все библиотеки из requirements.txt

Создайде базу данных и таблицу в ней:
`CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    id_telegram BIGINT UNIQUE NOT NULL,
    privacykey TEXT,
    address TEXT
);`

Заполните .env:

`BOT_TOKEN=ваш_токен_бота

SALT=ваша_соль_для_шифрования

DB_USER=ваш_пользователь
DB_PASSWORD=ваш_пароль
DB_NAME=имя_бд
DB_HOST=localhost
DB_PORT=5432`


Запуск происходит через Bot.py
