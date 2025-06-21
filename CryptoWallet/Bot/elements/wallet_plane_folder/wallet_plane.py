import asyncio


from aiogram import Router

from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.types import (
    InlineKeyboardMarkup, # клавиатура под сообщениями
    InlineKeyboardButton, # кнопки InlineKeyboardMarkup
)

from Bot.elements.settings_plane_folder import settings_plane

from database import database_func

from Bot.blockchain.BSC.BNB import utils
from Bot.blockchain.BSC import balance

router=Router()


# Функция для отправки в wallet
async def send_to_wallet(bot:Bot,chat_id, message_id=None):
    if (await database_func.check_wallet_in_db(chat_id)) == True:
        url = "https://bscscan.com/address/" + await database_func.get_address(chat_id)
        wallet = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Отправить", callback_data="transfer")
                ],
                [
                    InlineKeyboardButton(text="Посмотреть транзакции", url=url)
                ],
                [
                    InlineKeyboardButton(text="Назад", callback_data="start")
                ],
            ],
            resize_keyboard=True,  # для адаптации размера кнопок
            one_time_keyboard=True,  # скрытие после использования
            input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
            selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
        )
        txts = f"<b>Кошелёк</b>\n\nВаш адрес:\n\n<code>Обработка запроса...</code>\n\n🔷 Ethereum: <code>Обработка запроса...</code>\n\n🟡 Binance Coin: <code>Обработка запроса...</code>\n\n🟢 Tether: <code>Обработка запроса...</code>\n\n🔵 Toncoin: <code>Обработка запроса...</code>\n\n🟠 Bitcoin: <code>Обработка запроса...</code>\n\n🔴 TRON: <code>Обработка запроса...</code>\n\n🟢 Solana: <code>Обработка запроса...</code>\n\n🟦 Litecoin: <code>Обработка запроса...</code>\n\n🔵 USD Coin: <code>Обработка запроса...</code>"
        if message_id is not None:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=txts)
        else:
            message = await bot.send_message(chat_id, text=txts)
            message_id = message.message_id
        adress = str(await database_func.get_address(chat_id))

        balances = await balance.get_all_balances(adress)
        USDinRUB = float(await utils.get_USD_in_RUB()) # котировка рубля
        
        balance_ETH = float(balances.get('ETH', 0))
        balance_BNB = float(await balance.get_balance_in_BNB(adress))
        balance_USDT = float(balances.get('USDT', 0))
        balance_TON = float(balances.get('TON', 0))
        balance_BTC = float(balances.get('BTC', 0))
        balance_TRX = float(balances.get('TRX', 0))
        balance_SOL = float(balances.get('SOL', 0))
        balance_LTC = float(balances.get('LTC', 0))
        balance_USDC = float(balances.get('USDC', 0))

        eth_price = await balance.get_ETH_in_USDT() or 0
        bnb_price = await balance.get_BNB_in_USDT() or 0
        ton_price = await balance.get_TON_in_USDT() or 0
        btc_price = await balance.get_BTC_in_USDT() or 0
        trx_price = await balance.get_TRX_in_USDT() or 0
        sol_price = await balance.get_SOL_in_USDT() or 0
        ltc_price = await balance.get_LTC_in_USDT() or 0

        eth_value = balance_ETH * eth_price
        bnb_value = balance_BNB * bnb_price
        usdt_value = balance_USDT * 1.0  
        ton_value = balance_TON * ton_price
        btc_value = balance_BTC * btc_price
        trx_value = balance_TRX * trx_price
        sol_value = balance_SOL * sol_price
        ltc_value = balance_LTC * ltc_price
        usdc_value = balance_USDC * 1.0  

        balance_ETH = f"{balance_ETH:.7f}"
        balance_BNB = f"{balance_BNB:.7f}"
        balance_USDT = f"{balance_USDT:.7f}"
        balance_TON = f"{balance_TON:.7f}"
        balance_BTC = f"{balance_BTC:.7f}"
        balance_TRX = f"{balance_TRX:.7f}"
        balance_SOL = f"{balance_SOL:.7f}"
        balance_LTC = f"{balance_LTC:.7f}"
        balance_USDC = f"{balance_USDC:.7f}"
        
        total_usd = (
            eth_value + bnb_value + usdt_value + ton_value + 
            btc_value + trx_value + sol_value + ltc_value + usdc_value
        )
        
        total_usd_f = f"{total_usd:.2f}"
        total_rub = total_usd * USDinRUB
        total_rub_f= f"{total_rub:.2f}"
        



        wallet_n = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"🔷 Ethereum:                   {balance_ETH}  ETH          |", callback_data=f"ETH_BSC:{balance_ETH}:{USDinRUB}")
                ],
                [
                    InlineKeyboardButton(text=f"🟡 Binance Coin:             {balance_BNB}  BNB          |", callback_data=f"BNB_BSC:{balance_BNB}:{USDinRUB}")
                ],
                [
                    InlineKeyboardButton(text=f"🟢 Tether:                       {balance_USDT}  USDT         |", callback_data=f"USDT_BSC:{balance_USDT}:{USDinRUB}")
                ],
                [
                    InlineKeyboardButton(text=f"🔵 Toncoin:                     {balance_TON}  TON          |", callback_data=f"TON_BSC:{balance_TON}:{USDinRUB}")
                ],
                [
                    InlineKeyboardButton(text=f"🟠 Bitcoin:                     {balance_BTC}  BTC           |", callback_data=f"BTC_BSC:{balance_BTC}:{USDinRUB}")
                ],
                [
                    InlineKeyboardButton(text=f"🔴 TRON:                        {balance_TRX}  TRX           |", callback_data=f"TRX_BSC:{balance_TRX}:{USDinRUB}")
                ],
                [
                    InlineKeyboardButton(text=f"🟢 Solana:                       {balance_SOL}  SOL          |", callback_data=f"SOL_BSC:{balance_SOL}:{USDinRUB}")
                ],
                [
                    InlineKeyboardButton(text=f"🟦 Litecoin:                    {balance_LTC}  LTC           |", callback_data=f"LTC_BSC:{balance_LTC}:{USDinRUB}")
                ],
                [
                    InlineKeyboardButton(text=f"🔵 USD Coin:                  {balance_USDC}  USDC       |", callback_data=f"USDC_BSC:{balance_USDC}:{USDinRUB}")
                ],
                [
                    InlineKeyboardButton(text="Посмотреть транзакции", url=url)
                ],
                [
                    InlineKeyboardButton(text="Назад", callback_data="start")
                ]
            ],
            resize_keyboard=True,  # для адаптации размера кнопок
            one_time_keyboard=True,  # скрытие после использования
            input_field_placeholder="Выберите одну из опций",  # текст в поле ввода во время наличия кнопок
            selective=True  # для групп/чатов, чтобы вызов кнопки был только у 1го пользователя
        )
        #txt =f"<b>Кошелёк</b>\n\nВаш адрес:\n\n<code>{adress}</code>\n\nБаланс в BNB: <code>{balance_BNB}</code>\n\nБаланс в USD: <code>{balanse_BNB_in_USD}</code>\n\nБаланс в RUB: <code>{balanse_BNB_in_RUB}</code>"
        txt = f"<b>Кошелёк</b>\n\nВаш адрес:\n\n<code>{adress}</code>\n\nОбщий баланс:  \n\nRUB: {total_rub_f} \n\nUSD: {total_usd_f} \n\nБалансы:\n"
        await bot.edit_message_text(chat_id=chat_id, 
                                    message_id=message_id, 
                                    text=txt, 
                                    reply_markup=wallet_n
                                    )
    else:
        if message_id is not None:
            txt = "У вас нет кошелька!"
            await bot.edit_message_text(chat_id=chat_id, 
                                        message_id=message_id, 
                                        text=txt
                                        )
            await asyncio.sleep(2)
            await settings_plane.send_to_settings(bot, 
                                                  chat_id, 
                                                  message_id
                                                  )
        else:
            txt = "У вас нет кошелька!"
            message = await bot.send_message(chat_id=chat_id, 
                                             text=txt
                                             )
            await asyncio.sleep(2)
            message_id = message.message_id
            await settings_plane.send_to_settings(bot, 
                                                  chat_id, 
                                                  message_id=message_id
                                                  )

# В wallet по команде /wallet
@router.message(Command("wallet"))
async def wallet_command(message: Message,bot:Bot):
   # await message.delete()
    await send_to_wallet(bot, 
                          message.chat.id
                          )
    
# В wallet через callback-кнопки
@router.callback_query(lambda query: query.data == 'wallet')
async def wallet_menu_callback(callback_query: types.CallbackQuery,bot:Bot):
    await callback_query.answer()
    await send_to_wallet(bot, 
                          callback_query.message.chat.id, 
                          callback_query.message.message_id
                          )

