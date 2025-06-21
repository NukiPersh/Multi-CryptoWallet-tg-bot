import asyncio

from aiogram import Router

from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from Bot.keyboards.transfer import transfer_check,back_to_wallet

from Bot.elements.settings_plane_folder import settings_plane

from database import database_func

from Bot.blockchain.BSC.BNB import utils, send_transaction

from Cryptography import cryptography_pkeys


router=Router()

class Transfer_BNB(StatesGroup):
    address = State()
    sum = State()
    wait = State()
    password = State()


# В перевод по команде /transfer
@router.message(Command("transfer"))
async def transfer_command(message: Message, state: FSMContext, bot: Bot):
    if (await database_func.check_wallet_in_db(message.chat.id)) == True:
        await state.set_state(Transfer_BNB.address)
        txt="Введи адресс получателя:"
        await bot.send_message(chat_id=message.chat.id,
                                text=txt,
                                reply_markup=back_to_wallet
                                )
    else:
        txt = "У вас нет кошелька!"
        message = await bot.send_message(chat_id=message.chat.id, 
                                         text=txt
                                         )
        await asyncio.sleep(2)
        await settings_plane.send_to_settings(bot, 
                                              message.chat.id, 
                                              message.message_id
                                              )
    
# В перевод через callback-кнопки
@router.callback_query(lambda query: query.data == 'transfer')
async def transfer_menu_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot,):
    if (await database_func.check_wallet_in_db(callback_query.message.chat.id)) == True:
        await state.set_state(Transfer_BNB.address)
        await callback_query.answer()
        await state.update_data(bot_message_id=callback_query.message.message_id)
        txt= "Введите адресс получателя:"
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
@router.message(Transfer_BNB.address)
async def fill_address_transfer(message: Message, state: FSMContext, bot: Bot):
    addr = message.text
    data = await state.get_data()
    bot_message_id = await asyncio.to_thread(data.get, 'bot_message_id')  # Получаем сохраненный message_id из состояния    
    if await utils.check_address_for_transfer(addr) ==True: #условие что это адрес
        await state.update_data(address=addr)
        await state.set_state(Transfer_BNB.sum)
        await message.delete()
        maxs = (await utils.get_balance_in_BNB(await database_func.get_address(message.chat.id)) - await utils.get_gas_price()*1.1)
        max_sum = await asyncio.to_thread(lambda: max(0, maxs))
        txt=f"Введите сумму в BNB:\nМаксимум: {max_sum}"
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=bot_message_id,
                                    text =txt,
                                    reply_markup=back_to_wallet
                                    )
    else:
        await message.delete()
        txt="Не верный адресс!"
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=bot_message_id,
                                    text=txt,
                                    reply_markup=back_to_wallet
                                    )
        
# В смену суммы перевода через callback-кнопки
@router.callback_query(lambda query: query.data == 'change_sum')
async def change_sum_transfer(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot,):
    maxs = (await utils.get_balance_in_BNB(await database_func.get_address(callback_query.message.chat.id)) - await utils.get_gas_price()*1.1)
    max_sum = await asyncio.to_thread(lambda: max(0, maxs)) 
    txt=f"Введите сумму в BNB:\nМаксимум: {max_sum}"
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text =txt,
                                reply_markup=back_to_wallet
                                )
    await state.set_state(Transfer_BNB.sum)

#обработка суммы и отправка в ввод пароля
@router.message(Transfer_BNB.sum)
async def fill_sum_transfer(message: Message, state: FSMContext, bot:Bot):
    summ = message.text
    data_from_state = await state.get_data()
    #bot_message_id = data_from_state.get('bot_message_id')  # Получаем сохраненный message_id из состояния
    bot_message_id = await asyncio.to_thread(data_from_state.get, 'bot_message_id')  # Получаем сохраненный message_id из состояния
    if float(summ) > 0 and summ.isdigit and (float(summ) <= (await utils.get_balance_in_BNB(await database_func.get_address(message.chat.id)) - await utils.get_gas_price()*1.1)):#проверка что это число и что денег хватит на балансе
        summ = message.text
        txt =f"<b>Информация о транзакции:</b>\n\nПолучатель:\n{data_from_state.get('address')}\n\nСумма: {summ} BNB"
        await state.update_data(sum= summ)
        await state.set_state(Transfer_BNB.wait)
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=bot_message_id,
                                    text=txt,
                                    reply_markup=transfer_check
                                    ) 
    else:
        await message.delete()
        txt = f"Не верная сумма! Вы не можете отправить {summ} BNB"
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text=txt,
            reply_markup=back_to_wallet
            )

# В подтверждение/ввод пароля  через callback-кнопки
@router.callback_query(lambda query: query.data == 'accept_transfer')
async def accept_transfer(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot,):
    await state.set_state(Transfer_BNB.password)
    txt="Введите пароль для подписания транзакции:"
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=txt,
                                reply_markup=back_to_wallet
                                )

#Обработка парооля и подписание транзакции
@router.message(Transfer_BNB.password)
async def password_accept_transfer(message: Message, state: FSMContext, bot:Bot):
    passw = message.text
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')  # Получаем сохраненный message_id из состояния
    if len(passw) > 3 and await utils.check_password_for_pk(message.chat.id,passw) :#проверка что это пароль
        passw = message.text
        await state.update_data(password = passw)
        data_from_state = await state.get_data()
        #функция подписи и отправки транзакции
        tx = await send_transaction.send_bnb(await cryptography_pkeys.decrypt_private_key(await database_func.get_privacy_key(message.chat.id), passw),
                                  receiver_address=await asyncio.to_thread(data_from_state.get, 'address'),
                                  amount_in_bnb=float(await asyncio.to_thread(data_from_state.get, 'sum'))
                                  )
        txt =f"Транзакция успешно отправлена в обработку блокчейном!"
        await asyncio.to_thread(lambda: print(f"Пользователь {message.chat.id} отправил транзакцию {tx}"))
        await state.clear()
        await message.delete()
        url = "https://bscscan.com/tx/" + tx #await database_func.get_address(message.chat.id) 
        success= InlineKeyboardMarkup(
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




