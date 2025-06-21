from aiogram import Router, Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Bot.blockchain.BSC.USDT import utils
from database import database_func

router = Router()

async def send_to_bnb_menu(bot: Bot, chat_id: int, balance_token: float, USDinRUB: float, message_id=None):
    adress = await database_func.get_address(chat_id)
    TOKENinUSD = balance_token * await utils.get_USDT_in_USDT()
    TOKENinRUB = TOKENinUSD * float(USDinRUB)
    url = "https://bscscan.com/token/0x55d398326f99059fF775485246999027B3197955?a=" + adress


    bnb_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отправить USDT", callback_data="transfer_USDT_BSC_plane")],
            [InlineKeyboardButton(text="История переводов", url=url)],
            [InlineKeyboardButton(text="Назад", callback_data="wallet")],
            [InlineKeyboardButton(text="Меню", callback_data="start")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите одну из опций", 
        selective=True
    )

    txt = f"<b>Меню USDT:</b>\n\nВаш адрес:\n\n<code>{adress}</code>\n\nБаланс в USDT: <code>{balance_token:.7f}</code>\n\nБаланс в USD: <code>{TOKENinUSD:.7f}</code>\n\nБаланс в RUB: <code>{TOKENinRUB:.7f}</code>"

    if message_id is not None:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=txt, reply_markup=bnb_menu)
    else:
        await bot.send_message(chat_id, text=txt, reply_markup=bnb_menu)

@router.callback_query(lambda query: query.data.startswith('USDT_BSC:'))
async def bnb_menu_callback(callback_query: types.CallbackQuery, bot: Bot):
    await callback_query.answer()
    data = callback_query.data.split(':')
    balance_token = float(data[1])
    USDinRUB = data[2]
    await send_to_bnb_menu(bot, callback_query.message.chat.id, balance_token, USDinRUB, callback_query.message.message_id)
