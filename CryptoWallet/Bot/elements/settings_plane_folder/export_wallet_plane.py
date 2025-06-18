import asyncio

from aiogram import Router

from aiogram import Bot, types
from aiogram.types import Message

from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from Bot.keyboards.settings import return_to_start, pass_in_export_wallet,wrong_password

from Bot.elements.settings_plane_folder import settings_plane

from Bot.blockchain.BSC.BNB import utils

from Cryptography import cryptography_pkeys

from database import database_func


router=Router()

class Export_wallet(StatesGroup):
    password = State()


# Функция для отправки в экспорт кошелька
async def send_to_export_wallet(bot:Bot, chat_id,message_id):
    txt ="Внимание, далее будут вводится секретные данные!"
    await bot.edit_message_text(chat_id=chat_id, 
                                message_id=message_id, 
                                text=txt, 
                                reply_markup=pass_in_export_wallet
                                ) 

# В экспорт кошелька через callback-кнопки
@router.callback_query(lambda query: query.data == 'export_wallet')
async def export_wallet_callback(callback_query: types.CallbackQuery, bot:Bot):
    if (await database_func.check_wallet_in_db(callback_query.message.chat.id) ==True):
        await send_to_export_wallet(bot, 
                                    callback_query.message.chat.id, 
                                    callback_query.message.message_id
                                    )
    else:
        txt ="У вас нет кошелька!"
        await bot.edit_message_text(text=txt,
                                    chat_id=callback_query.message.chat.id, 
                                    message_id=callback_query.message.message_id
                                    )
        await asyncio.sleep(2)
        await settings_plane.send_to_settings(bot, 
                                              callback_query.message.chat.id, 
                                              callback_query.message.message_id
                                              )

#В ввод пароля
@router.callback_query(lambda query: query.data == 'export_wallet_password')
async def post_fill_password(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(Export_wallet.password)
    await state.update_data(bot_message_id=callback_query.message.message_id)
    txt = "Введи пароль:"
    await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=txt,
            reply_markup=return_to_start
            )

#Успех
@router.message(Export_wallet.password)
async def fill_password(message: Message, state: FSMContext, bot:Bot):
    password  = message.text
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')  # Получаем сохраненный message_id из состояния
    if len(password) > 3 and (await utils.check_password_for_pk(message.chat.id, password)):#проверка что это пароль
        await state.clear()
        await message.delete()
        encrypted_pk = await database_func.get_privacy_key(message.chat.id)
        decrypted_pk = await cryptography_pkeys.decrypt_private_key(encrypted_pk, password)
        txt=f"<b>Ваш кошелёк!</b>\n\nВаш приватный ключ:\n\n<code>{decrypted_pk}</code>\n\nВаш пароль:\n\n<code>{password}</code>\n\n\n<b>Сохраните эти данные!</b>"
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=txt,
            reply_markup=return_to_start
            ) 
    else:
        await message.delete()
        txt = "Не верный пароль!\n Введите еще раз"
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=txt,
            reply_markup=wrong_password
            )
