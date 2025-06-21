from aiogram import Router

from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.types import Message

from Bot.keyboards.start_list import start_kb

from database import database_func


router=Router()


# Функция для отправки старта
async def send_to_start(bot: Bot, chat_id, message_id=None):
    txt = f"<b>📒 Multi Wallet 📒</b>\n\nМультивалютный DEX криптокошелёк\n\nХраните, получайте, отправляйте криптовалюту, когда хотите.\n\n Першин Н.Г. КубГу"
    if message_id is not None:#если сообщение уже существует, то просто редактируем его
        await bot.edit_message_text(chat_id=chat_id, #айди чата
                                    message_id=message_id, #айди сообщения из чата
                                    text=txt, #текст, на который будет заменен текущий текст
                                    reply_markup=start_kb, # клавиатура, на которую будет заменена текущая клавиатура
                                    )
    else: # если сообщения не существует, то отправляем новое
        await bot.send_message(chat_id=chat_id, 
                               text=txt, 
                               reply_markup=start_kb
                               )

# В старт по команде /start
@router.message(Command("start"))
async def start_command(message: Message, bot: Bot):
    await database_func.add_new_user(message.chat.id
                                     ) # добавляем айди пользователя в базу данных, если не нашли пользователя в ней
    await send_to_start(bot, 
                        message.chat.id
                        )# оправляем в функцию отправки старта

# В старт через callback-кнопки
@router.callback_query(lambda query: query.data == 'start')
async def start_menu_callback(callback_query: types.CallbackQuery, bot: Bot):
    #не добавляем в бд, тк при первом запуске пользователь всегда нажимает /start
    await send_to_start(bot, 
                        callback_query.message.chat.id, 
                        callback_query.message.message_id
                        )# оправляем в функцию отправки старта


