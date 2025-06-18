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

        

        # Получаем сразу все балансы в одном запросе

        balances = await balance.get_all_balances(adress)
        USDinRUB = float(await utils.get_USD_in_RUB()) # котировка рубля
        

        balance_ETH = f"{float(balances.get('ETH', 0)):.7f}"
        balance_BNB = f"{float(await balance.get_balance_in_BNB(adress)):.7f}"
        balance_USDT = f"{float(balances.get('USDT', 0)):.7f}"
        balance_TON = f"{float(balances.get('TON', 0)):.7f}"
        balance_BTC = f"{float(balances.get('BTC', 0)):.7f}"
        balance_TRX = f"{float(balances.get('TRX', 0)):.7f}"
        balance_SOL = f"{float(balances.get('SOL', 0)):.7f}"
        balance_LTC = f"{float(balances.get('LTC', 0)):.7f}"
        balance_USDC = f"{float(balances.get('USDC', 0)):.7f}"

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
        txt = f"<b>Кошелёк</b>\n\nВаш адрес:\n\n<code>{adress}</code>\n\nБалансы:\n"
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

