from aiogram.types import (
    InlineKeyboardMarkup, # клавиатура под сообщениями
    InlineKeyboardButton, # кнопки InlineKeyboardMarkup
)

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Кошелёк", callback_data="wallet")
        ],
        [
            InlineKeyboardButton(text="Настройки", callback_data="settings")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)


