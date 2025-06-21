from aiogram import Router, Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Bot.blockchain.BSC.BNB import utils
from database import database_func

router = Router()

async def send_to_bnb_menu(bot: Bot, chat_id: int, balance_bnb: float, USDinRUB: float, message_id=None):
    adress = await database_func.get_address(chat_id)
    BNBinUSD = balance_bnb * await utils.get_BNB_in_USDT()
    BNBinRUB = BNBinUSD * float(USDinRUB)
    url = "https://bscscan.com/address/" + adress

    bnb_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отправить BNB", callback_data="transfer_BNB_BSC_plane")],
            [InlineKeyboardButton(text="История переводов", url=url)],
            [InlineKeyboardButton(text="Назад", callback_data="wallet")],
            [InlineKeyboardButton(text="Меню", callback_data="start")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите одну из опций", 
        selective=True
    )

    txt = f"<b>Меню BNB:</b>\n\nВаш адрес:\n\n<code>{adress}</code>\n\nБаланс в BNB: <code>{balance_bnb:.7f}</code>\n\nБаланс в USD: <code>{BNBinUSD:.7f}</code>\n\nБаланс в RUB: <code>{BNBinRUB:.7f}</code>"

    if message_id is not None:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=txt, reply_markup=bnb_menu)
    else:
        await bot.send_message(chat_id, text=txt, reply_markup=bnb_menu)

@router.callback_query(lambda query: query.data.startswith('BNB_BSC:'))
async def bnb_menu_callback(callback_query: types.CallbackQuery, bot: Bot):
    await callback_query.answer()
    data = callback_query.data.split(':')
    balance_bnb = float(data[1])
    USDinRUB = data[2]
    await send_to_bnb_menu(bot, callback_query.message.chat.id, balance_bnb, USDinRUB, callback_query.message.message_id)