from aiogram import Router

from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.types import Message

from Bot.keyboards.settings import settings

from database import database_func

router=Router()

# Функция для отправки настроек
async def send_to_settings(bot: Bot, chat_id, message_id=None):
    if (await database_func.check_wallet_in_db(chat_id)) == True:#если есть кошеклек, то в тексте будет кошелек, иначе нет
        address = await database_func.get_address(chat_id)
        txt=f"<b>Настройки</b>\n\nВаш кошелек:\n\n<code>{address}</code>"
    else:
        txt=f"<b>Настройки</b>\n\nУ вас нет кошелька"
    if message_id is not None:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=txt, reply_markup=settings)
    else:
        await bot.send_message(chat_id, text=txt, reply_markup=settings)

# В настройки по команде /settings
@router.message(Command("settings"))
async def settings_command(message: Message, bot: Bot):
    await send_to_settings(bot, 
                           message.chat.id
                           )
    
# В настройки через callback-кнопки
@router.callback_query(lambda query: query.data == 'settings')
async def settings_menu_callback(callback_query: types.CallbackQuery,bot: Bot):
    await send_to_settings(bot, 
                           callback_query.message.chat.id, 
                           callback_query.message.message_id
                           )

