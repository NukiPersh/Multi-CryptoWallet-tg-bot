from aiogram.types import (
    ReplyKeyboardMarkup, # клавиатура под полем ввода
    KeyboardButton, # кнопки ReplyKeyboardMarkup
    InlineKeyboardMarkup, # клавиатура под сообщениями
    InlineKeyboardButton, # кнопки InlineKeyboardMarkup
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from aiogram.filters.callback_data import CallbackData

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Импорт кошелька", callback_data="import_wallet")
        ],
        [
            InlineKeyboardButton(text="Экспорт кошелька", callback_data="export_wallet")
        ],
        [
            InlineKeyboardButton(text="Создать кошелёк", callback_data="create_wallet")
        ],
        [
            InlineKeyboardButton(text="Удалить кошелек", callback_data="delete_wallet")
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

import_wallet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Меню", callback_data="start")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="settings")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)

pass_in_import_wallet= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продолжить", callback_data="add_wallet")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="import_wallet")
        ],
        [
            InlineKeyboardButton(text="Меню", callback_data="start")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)

export_wallet= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Меню", callback_data="start")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="settings")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)

pass_in_export_wallet= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Меню", callback_data="start")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)
pass_in_create_wallet= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продолжить", callback_data="create_wallet_create_password")
        ],
        [
            InlineKeyboardButton(text="Меню", callback_data="start")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)


post_pass_in_delete_wallet= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="delete_wallet_password"),
            InlineKeyboardButton(text="Нет", callback_data="settings")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)

return_to_start=InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Меню", callback_data="start"),
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)

pass_in_export_wallet= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продолжить", callback_data="export_wallet_password")
        ],
        [
            InlineKeyboardButton(text="Меню", callback_data="start")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)
pass_in_export_wallet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продолжить", callback_data="export_wallet_password")
        ],
        [
            InlineKeyboardButton(text="Меню", callback_data="start")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)
pass_in_import_wallet= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продолжить", callback_data="import_wallet_password")
        ],
        [
            InlineKeyboardButton(text="Меню", callback_data="start")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)

wrong_password = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Меню", callback_data="start")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)