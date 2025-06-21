from aiogram import Router

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from Bot.keyboards.wallet import recieve


from Bot.elements.settings_plane_folder import settings_plane


router=Router()


# Функция для отправки в recieve
async def send_to_recieve(bot:Bot,chat_id, message_id=None):
    if 1==1:    
        adress="достаем из бд"
        txt =f"Ваш адрес:\n\n{adress}"
        if message_id is not None:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=txt, reply_markup=recieve)
        else:
            await bot.send_message(chat_id, text=txt, reply_markup=recieve)
    else:
        settings_plane.send_to_settings(chat_id)

# В recieve через callback-кнопки
@router.callback_query(lambda query: query.data == 'recieve')
async def wallet_menu_callback(callback_query: types.CallbackQuery,bot:Bot):
    await callback_query.answer()
    await send_to_recieve(bot, callback_query.message.chat.id, callback_query.message.message_id)

