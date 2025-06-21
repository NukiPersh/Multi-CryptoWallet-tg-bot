import asyncio

from aiogram import Router

from aiogram import Bot, types
from aiogram.types import Message

from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from Bot.keyboards.settings import wrong_password, pass_in_create_wallet, return_to_start

from Bot.elements.settings_plane_folder import settings_plane

from Bot.blockchain.BSC.BNB import utils

from Cryptography import cryptography_pkeys

from database import database_func


router=Router()

class Create_wallet(StatesGroup):
    input = State()


# Функция для отправки в кошелёк
async def send_to_create_wallet(bot:Bot, chat_id,message_id):
    txt=f"Далее будут выведены секретные данные, которые никто кроме вас не должен знать!"
    await bot.edit_message_text(chat_id=chat_id, 
                                message_id=message_id, 
                                text=txt, 
                                reply_markup=pass_in_create_wallet
                                ) 

# В создание кошелька через callback-кнопки
@router.callback_query(lambda query: query.data == 'create_wallet')
async def create_wallet_callback(callback_query: types.CallbackQuery, bot:Bot):
    if (await database_func.check_wallet_in_db(callback_query.message.chat.id) ==False):#проверка на наличие кошелька в бд по tg_id
        await send_to_create_wallet(bot,
                                    callback_query.message.chat.id, 
                                    callback_query.message.message_id
                                    )
    else:
        await bot.edit_message_text(text="У вас есть кошелёк!", 
                                    chat_id=callback_query.message.chat.id, 
                                    message_id=callback_query.message.message_id
                                    )
        await asyncio.sleep(2)
        await settings_plane.send_to_settings(bot, 
                                              callback_query.message.chat.id, 
                                              callback_query.message.message_id
                                              )
#В ввод пароля
@router.callback_query(lambda query: query.data == 'create_wallet_create_password')
async def post_fill_password(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(Create_wallet.input)
    await state.update_data(bot_message_id=callback_query.message.message_id)
    await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Введи пароль для своего кошелька",
            reply_markup=return_to_start
            )
    
#Вызов после ввода пароля
@router.message(Create_wallet.input)
async def fill_password(message: Message, state: FSMContext, bot:Bot):
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')  # Получаем сохраненный message_id из состояния
    password = message.text
    if len(password) > 3:#проверка что пароль подходит для шифрования PK
        seed= str(await utils.get_generate_bnb_seed_phrase())
        priv_key, address = await utils.get_create_wallet_from_mnemonic(seed)
        encrypted_pk = await cryptography_pkeys.encrypt_private_key(priv_key, 
                                                                    password
                                                                    )
        await database_func.add_wallet_to_db(message.chat.id, 
                                             encrypted_pk, 
                                             address
                                             )
        txt=f"<b>Вы создали кошелек!</b>\n\nВаша сид фраза:\n\n<tg-spoiler>{seed}</tg-spoiler>\n \nВаш приватный ключ:\n\n<code>{priv_key}</code>\n \nВаш пароль:\n\n<code>{password}</code>\n\n\n<b>Сохраните эти данные!</b>"
        await state.clear()
        await message.delete()
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=txt,
            reply_markup=return_to_start
            ) 
    else:
        await message.delete()
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text="Не верный формат!\nВведите пароль еще раз",
            reply_markup=wrong_password
            )


