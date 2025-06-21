import asyncio
import random
from aiogram import Router

from aiogram import Bot, types
from aiogram.types import Message

from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from Bot.keyboards.settings import post_pass_in_delete_wallet,return_to_start,wrong_password

from Bot.elements.settings_plane_folder import settings_plane

from database import database_func


router=Router()

class Delete_wallet(StatesGroup):
    input = State()


# Функция для отправки в удаление кошелька
async def send_to_delete_wallet(bot:Bot,chat_id,message_id):
    txt="Вы уверены что хотите удалить кошелек?"
    await bot.edit_message_text(chat_id=chat_id, 
                                message_id=message_id, 
                                text=txt, 
                                reply_markup=post_pass_in_delete_wallet
                                ) 
    
#В удаление кошелька через callback-кнопки
@router.callback_query(lambda query: query.data == 'delete_wallet')
async def export_wallet_callback(callback_query: types.CallbackQuery,bot: Bot):
    if (await database_func.check_wallet_in_db(callback_query.message.chat.id) ==True):#проверка на наличие кошелька в бд
        await send_to_delete_wallet(bot, 
                                    callback_query.message.chat.id, 
                                    callback_query.message.message_id)
    else:
        txt = "У вас нет кошелька!"
        await bot.edit_message_text(text=txt,
                                    chat_id=callback_query.message.chat.id, 
                                    message_id=callback_query.message.message_id)
        await asyncio.sleep(2)
        await settings_plane.send_to_settings(bot, 
                                              callback_query.message.chat.id, 
                                              callback_query.message.message_id)

#Ввод кода для удаления кошелька
@router.callback_query(lambda query: query.data == 'delete_wallet_password')
async def post_fill_password(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(Delete_wallet.input)
    await state.update_data(bot_message_id=callback_query.message.message_id)
    rand = ''.join(random.choices('0123456789', k=5))
    await state.update_data(for_delete = rand)
    txt= f"Введи {rand} чтобы удалить свой кошелек"
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=txt,
                                reply_markup=return_to_start
                                )

#Успех удаления
@router.message(Delete_wallet.input)
async def fill_password(message: Message, state: FSMContext, bot:Bot):
    passw = str(message.text)
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')  # Получаем сохраненный message_id из состояния
    password = str(data.get('for_delete'))
    if passw ==password:#проверка что код подходит
        await database_func.delete_wallet_from_db(message.chat.id)
        txt=f"Кошелек удален"
        await state.clear()
        await message.delete()
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id = bot_message_id,
            text=txt,
            reply_markup=return_to_start) 
    else:
        await message.delete()
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id = bot_message_id,
            text=f"Не верный код!\nВведите код еще раз:\n{password}",
            reply_markup=wrong_password
            )


    
    
