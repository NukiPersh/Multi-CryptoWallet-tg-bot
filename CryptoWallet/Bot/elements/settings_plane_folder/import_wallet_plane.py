import asyncio

from aiogram import Router

from aiogram import Bot, types
from aiogram.types import Message

from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from Bot.keyboards.settings import return_to_start,pass_in_import_wallet

from Bot.elements.settings_plane_folder import settings_plane

from database import database_func

from Cryptography import cryptography_pkeys

from Bot.blockchain.BSC.BNB import utils


router=Router()

class Import_wallet(StatesGroup):
    seed_phrase = State()
    privacy_key = State()
    password = State()


# Функция для отправки в экспорт кошелька
async def send_to_import_wallet(bot:Bot, chat_id,message_id):
    txt = "Внимание, далее будут вводится секретные данные!"
    await bot.edit_message_text(chat_id=chat_id, 
                                message_id=message_id, 
                                text=txt, 
                                reply_markup=pass_in_import_wallet
                                ) 

# В экспорт кошелька через callback-кнопки
@router.callback_query(lambda query: query.data == 'import_wallet')
async def import_wallet_callback(callback_query: types.CallbackQuery, bot:Bot):
    if (await database_func.check_wallet_in_db(callback_query.message.chat.id)) == False:
        await send_to_import_wallet(bot, 
                                    callback_query.message.chat.id, 
                                    callback_query.message.message_id
                                    )
    else:
        txt ="У вас есть кошелек!"
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                    message_id=callback_query.message.message_id, 
                                    text=txt
                                    )
        await asyncio.sleep(2)
        await settings_plane.send_to_settings(bot, 
                                              callback_query.message.chat.id, 
                                              callback_query.message.message_id
                                              )

#В ввод сид фразы или приватного ключа
@router.callback_query(lambda query: query.data == 'import_wallet_password')
async def post_fill_password(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(Import_wallet.seed_phrase)
    await state.update_data(bot_message_id=callback_query.message.message_id)
    txt ="Введи сид фразу или приватный ключ для своего кошелька"
    await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=txt,
            reply_markup=return_to_start
            )

#Обработка сид фразы или приватного ключа и отправка в ввод пароля
@router.message(Import_wallet.seed_phrase)
async def fill_password(message: Message, state: FSMContext, bot:Bot):
    seed = message.text
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')  # Получаем сохраненный message_id из состояния
    if (await utils.check_on_seed_phrase(seed)) == True:#проверка что это сид фраза
        seed = message.text
        await state.update_data(seed_phrase=seed)
        txt =f"Введите пароль, минимальная длина 4 символа."
        await state.set_state(Import_wallet.password)
        await message.delete()
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=txt,
            ) 
    elif (await utils.check_on_privacykey(seed)) == True:#проверка что это приватный ключ
        privkey = message.text
        await state.update_data(privacy_key=privkey)
        txt =f"Введите пароль, минимальная длина 4 символа."
        await state.set_state(Import_wallet.password)
        await message.delete()
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=txt,
            ) 
    else:
        await message.delete()
        txt = "Не верно!\nВведите сид фразу или приватный ключ еще раз"
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=txt,
            reply_markup=return_to_start
            )

#обработка пароля и завершение импорта
@router.message(Import_wallet.password)
async def final_import(message: Message, state: FSMContext, bot:Bot):
    passw = message.text
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')  # Получаем сохраненный message_id из состояния
    if len(passw) > 3:#проверка что пароль подходит для шифрования PK
        password= message.text
        await state.update_data(password=passw)
        data_from_state = await state.get_data()
        try:
            seed = data_from_state.get('seed_phrase')#пробуем получить приватный ключ
            priv_key,address =await utils.get_create_wallet_from_mnemonic(seed)
            encrypted_pk = await cryptography_pkeys.encrypt_private_key(priv_key, password)
            await database_func.add_wallet_to_db(message.chat.id, encrypted_pk, address)
            txt=f"<b>Вы импортировали кошелек!</b>\n\nВаша сид фраза:\n\n<tg-spoiler>{seed}</tg-spoiler>\n \nВаш приватный ключ:\n\n<code>{priv_key}</code>\n \nВаш пароль:\n\n<code>{password}</code>\n\n\n<b>Сохраните эти данные!</b>"
            await state.clear()
            await message.delete()
        except:
            priv_key = data_from_state.get('privacy_key')
            address =await utils.get_address_from_pk(priv_key)
            encrypted_pk = await cryptography_pkeys.encrypt_private_key(priv_key, password)
            await database_func.add_wallet_to_db(message.chat.id, encrypted_pk, address)
            txt=f"<b>Вы импортировали кошелек!</b>\n\nВаш приватный ключ:\n\n<code>{priv_key}</code>\n \nВаш пароль:\n\n<code>{password}</code>\n\n\n<b>Сохраните эти данные!</b>"
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
            text="Не верный формат!\n Введите пароль еще раз",
            reply_markup=return_to_start
            )





