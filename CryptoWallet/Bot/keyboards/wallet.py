from aiogram.types import (
    ReplyKeyboardMarkup, # клавиатура под полем ввода
    KeyboardButton, # кнопки ReplyKeyboardMarkup
    InlineKeyboardMarkup, # клавиатура под сообщениями
    InlineKeyboardButton, # кнопки InlineKeyboardMarkup
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from aiogram.filters.callback_data import CallbackData

wallet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отправить", callback_data="transfer")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)

recieve = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="wallet"),
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)