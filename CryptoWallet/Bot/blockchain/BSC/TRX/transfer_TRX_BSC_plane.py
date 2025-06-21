import asyncio

from aiogram import Router

from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from Bot.keyboards.transfer import back_to_wallet

from Bot.elements.settings_plane_folder import settings_plane

from database import database_func

from Bot.blockchain.BSC.TRX import utils, send_transaction
from Bot.blockchain.BSC import balance
from Cryptography import cryptography_pkeys


router = Router()

class Transfer_TRX_BSC(StatesGroup):
    address = State()
    sum = State()
    wait = State()
    password = State()

trxtoken = "0xCE7de646e7208a4Ef112cb6ed5038FA6cC6b12e3"

# В перевод через callback-кнопки
@router.callback_query(lambda query: query.data == 'transfer_TRX_BSC_plane')
async def transfer_menu_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot,):
    if (await database_func.check_wallet_in_db(callback_query.message.chat.id)) == True:
        await state.set_state(Transfer_TRX_BSC.address)
        await callback_query.answer()
        await state.update_data(bot_message_id=callback_query.message.message_id)
        txt = "Введите адресс получателя TRX (СЕТЬ BSC):"
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=txt,
                                    reply_markup=back_to_wallet
                                    )
    else:
        txt = "У вас нет кошелька!"
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                    message_id=callback_query.message.message_id, 
                                    text=txt
                                    )
        await asyncio.sleep(2)
        await settings_plane.send_to_settings(bot, 
                                              callback_query.message.chat.id,
                                              callback_query.message.message_id
                                              )

#обработка ввода адреса и отправка на ввод суммы
@router.message(Transfer_TRX_BSC.address)
async def fill_address_transfer(message: Message, state: FSMContext, bot: Bot):
    addr = message.text
    data = await state.get_data()
    bot_message_id = await asyncio.to_thread(data.get, 'bot_message_id')  # Получаем сохраненный message_id из состояния    
    if await utils.check_address_for_transfer(addr) == True: #условие что это адрес
        await state.update_data(address=addr)
        await state.set_state(Transfer_TRX_BSC.sum)
        await message.delete()
        maxs = await balance.get_token_balance(await database_func.get_address(message.chat.id), trxtoken)
        max_sum = await asyncio.to_thread(lambda: max(0, maxs))
        txt = f"Введите сумму в TRX:\nМаксимум: {max_sum}"
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=bot_message_id,
                                    text=txt,
                                    reply_markup=back_to_wallet
                                    )
    else:
        await message.delete()
        txt = "Не верный адресс!"
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=bot_message_id,
                                    text=txt,
                                    reply_markup=back_to_wallet
                                    )

# В смену суммы перевода через callback-кнопки
@router.callback_query(lambda query: query.data == 'change_sum_bsc_trx')
async def change_sum_transfer(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot,):
    maxs = (await balance.get_token_balance(await database_func.get_address(callback_query.message.chat.id), trxtoken))
    max_sum = await asyncio.to_thread(lambda: max(0, maxs)) 
    txt = f"Введите сумму в TRX:\nМаксимум: {max_sum}"
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=txt,
                                reply_markup=back_to_wallet
                                )
    await state.set_state(Transfer_TRX_BSC.sum)

#обработка суммы и отправка в ввод пароля
@router.message(Transfer_TRX_BSC.sum)
async def fill_sum_transfer(message: Message, state: FSMContext, bot:Bot):
    summ = message.text
    summ = summ.replace(',', '.')
    data_from_state = await state.get_data()
    bot_message_id = await asyncio.to_thread(data_from_state.get, 'bot_message_id')  # Получаем сохраненный message_id из состояния
    if float(summ) > 0 and summ.isdigit and (float(summ) <= (await balance.get_token_balance(await database_func.get_address(message.chat.id), trxtoken))):#проверка что это число и что денег хватит на балансе
        txt = f"<b>Информация о транзакции:</b>\n\nПолучатель:\n{data_from_state.get('address')}\n\nСумма: {summ} TRX"
        await state.update_data(sum=summ)
        await state.set_state(Transfer_TRX_BSC.wait)
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=bot_message_id,
                                    text=txt,
                                    reply_markup=transfer_check_trx
                                    ) 
    else:
        await message.delete()
        txt = f"Не верная сумма! Вы не можете отправить {summ} TRX"
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=txt,
            reply_markup=back_to_wallet
            )

# В подтверждение/ввод пароля  через callback-кнопки
@router.callback_query(lambda query: query.data == 'accept_transfer_bsc_trx')
async def accept_transfer(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot,):
    await state.set_state(Transfer_TRX_BSC.password)
    txt = "Введите пароль для подписания транзакции:"
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=txt,
                                reply_markup=back_to_wallet
                                )

#Обработка парооля и подписание транзакции
@router.message(Transfer_TRX_BSC.password)
async def password_accept_transfer(message: Message, state: FSMContext, bot:Bot):
    passw = message.text
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')  # Получаем сохраненный message_id из состояния
    if len(passw) > 3 and await utils.check_password_for_pk(message.chat.id, passw):#проверка что это пароль
        passw = message.text
        await state.update_data(password=passw)
        data_from_state = await state.get_data()
        #функция подписи и отправки транзакции
        tx = await send_transaction.send_token_trx(await cryptography_pkeys.decrypt_private_key(await database_func.get_privacy_key(message.chat.id), passw),
                                  receiver_address=await asyncio.to_thread(data_from_state.get, 'address'),
                                  amount_in_token=float(await asyncio.to_thread(data_from_state.get, 'sum'))
                                  )
        txt = f"Транзакция успешно отправлена в обработку блокчейном!"
        await asyncio.to_thread(lambda: print(f"Пользователь {message.chat.id} отправил транзакцию {tx}"))
        await state.clear()
        await message.delete()
        url = "https://bscscan.com/tx/" + tx 
        success = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Посмотреть транзакцию", url=url)
                        ],
                        [
                            InlineKeyboardButton(text="Меню", callback_data="start")
                        ],
                    ],
                resize_keyboard=True,  # для адаптации размера кнопок
                one_time_keyboard=True,  # скрытие после использования
                input_field_placeholder="Выберите одну из опций",# текст в поле ввода во время наличия кнопок
                selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
            )
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=bot_message_id,
                                    text=txt,
                                    reply_markup=success
                                    ) 
    else:
        await message.delete()
        txt = "Не верный пароль!"
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=bot_message_id,
                                    text=txt,
                                    reply_markup=back_to_wallet
                                    )




transfer_check_trx = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data="accept_transfer_bsc_trx")
        ],
        [
            InlineKeyboardButton(text="Изменить сумму", callback_data="change_sum_bsc_trx")
        ],
    ],
    resize_keyboard=True,  # для адаптации размера кнопок
    one_time_keyboard=True,  # скрытие после использования
    input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
    selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
)