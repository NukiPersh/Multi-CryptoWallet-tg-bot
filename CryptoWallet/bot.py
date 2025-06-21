#импорт библиотек, конфига, модулей:
import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
import logging

from Bot.elements.start_plane_folder import(
    start_plane
)

from Bot.elements.settings_plane_folder import (
    settings_plane,
    create_wallet_plane, 
    delete_wallet_plane, 
    export_wallet_plane,
    import_wallet_plane
)

from Bot.elements.wallet_plane_folder import(
    wallet_plane,
    recieve_plane
)

#блок BSC
from Bot.blockchain.BSC.ETH import(

        #ETH
    ETH_BSC_plane,
    transfer_ETH_BSC_plane
)
from Bot.blockchain.BSC.BNB import(#
        #BNB
    BNB_BSC_plane,
    transfer_BNB_BSC_plane
)
from Bot.blockchain.BSC.USDT import(
        #USDT
    USDT_BSC_plane,
    transfer_USDT_BSC_plane
)
from Bot.blockchain.BSC.TON import(
        #TON
    TON_BSC_plane,
    transfer_TON_BSC_plane
)
from Bot.blockchain.BSC.BTC import(
        #BTC
    BTC_BSC_plane,
    transfer_BTC_BSC_plane
)
from Bot.blockchain.BSC.TRX import(
        #TRX
    TRX_BSC_plane,
    transfer_TRX_BSC_plane
)
from Bot.blockchain.BSC.SOL import(
        #SOL
    SOL_BSC_plane,
    transfer_SOL_BSC_plane
)
from Bot.blockchain.BSC.LTC import(
        #LTC
    LTC_BSC_plane,
    transfer_LTC_BSC_plane
)
from Bot.blockchain.BSC.USDC import(
        #USDC
    USDC_BSC_plane,
    transfer_USDC_BSC_plane
)

from database.database_func import create_db_pool, close_db_pool

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def on_startup():
    await create_db_pool()
    logger.info("Bot started")

async def on_shutdown():
    await close_db_pool()
    logger.info("Bot stopped")


async def main():
    bot=Bot(config.bot_token.get_secret_value(), parse_mode="HTML") # инициализация бота, передача токена и метода отправки сообщений
    dp = Dispatcher() #инициализация диспетчера

    # Обработчики запуска/остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(#добавляем роутеры (модули бота из других файло)
        #элементы с / - коммандами
        start_plane.router,
        settings_plane.router,
        wallet_plane.router,

        #блок start

        #блок  settings
        create_wallet_plane.router,
        delete_wallet_plane.router,
        export_wallet_plane.router,
        import_wallet_plane.router,

        #блок wallet
        recieve_plane.router,

        #блок BSC
        #ETH
        ETH_BSC_plane.router,
        transfer_ETH_BSC_plane.router,

        #BNB
        BNB_BSC_plane.router,
        transfer_BNB_BSC_plane.router,

        #USDT
        USDT_BSC_plane.router,
        transfer_USDT_BSC_plane.router,

        #TON
        TON_BSC_plane.router,
        transfer_TON_BSC_plane.router,

        #BTC
        BTC_BSC_plane.router,
        transfer_BTC_BSC_plane.router,

        #TRX
        TRX_BSC_plane.router,
        transfer_TRX_BSC_plane.router,

        #SOL
        SOL_BSC_plane.router,
        transfer_SOL_BSC_plane.router,

        #LTC
        LTC_BSC_plane.router,
        transfer_LTC_BSC_plane.router,

        #USDC
        USDC_BSC_plane.router,
        transfer_USDC_BSC_plane.router


    )
    await bot.delete_webhook(drop_pending_updates=True)#чистим запросы, полученные во время отключения бота
    logger.info("Starting polling...")
    await dp.start_polling(bot) #запуск бота


if __name__ == "__main__": #главный запуск, срабатывает при открытии данного файла
    asyncio.run(main()) 