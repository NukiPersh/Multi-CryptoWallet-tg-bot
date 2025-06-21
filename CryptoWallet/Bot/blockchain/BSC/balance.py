from web3 import AsyncWeb3, Web3
import asyncio
from config_reader import config
import aiohttp
from typing import Optional

BSC_NODE = "https://bsc-dataseed1.binance.org:443"
web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(BSC_NODE))

ERC20_ABI = '''
[
    {"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},
    {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}
]
'''

async def get_balance_in_BNB(address):
    balance = await web3.eth.get_balance(address)
    return balance / 10**18  
async def get_token_balance(address, token_address):
    try:
        address = Web3.to_checksum_address(address)
        token_address = Web3.to_checksum_address(token_address)
        
        contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
        
        balance = await contract.functions.balanceOf(address).call()
        decimals = await contract.functions.decimals().call()
        
        return balance / (10**decimals)

    except Exception as e:
        await asyncio.to_thread(lambda: print(f"Ошибка при получении баланса токена {token_address}: {str(e)}"))
        return 0.0

async def get_all_balances(address):
    """Получаем все балансы для указанного адреса"""
    contracts = {
        "BNB": None,  # Нативный BNB
        "ETH": "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
        "USDT": "0x55d398326f99059fF775485246999027B3197955",
        "TON": "0x76A797A59Ba2C17726896976B7B3747BfD1d220f",
        "BTC": "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
        "TRX": "0xCE7de646e7208a4Ef112cb6ed5038FA6cC6b12e3",
        "SOL": "0x570A5D26f7765Ecb712C0924E4De545B89fD43dF",
        "LTC": "0x4338665CBB7B2485A8855A139b75D5e34AB0DB94",
        "USDC": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"
    }
    
    results = {}
    
    # Получаем баланс BNB отдельно
    if "BNB" in contracts:
        results["BNB"] = await get_balance_in_BNB(address)
        del contracts["BNB"]
    
    # Получаем балансы токенов
    tasks = []
    for token, contract_address in contracts.items():
        tasks.append(get_token_balance(address, contract_address))
    
    balances = await asyncio.gather(*tasks)
    
    # Формируем результаты
    for token, balance in zip(contracts.keys(), balances):
        results[token] = balance
    
    return results



async def get_crypto_price(symbol: str) -> Optional[float]:
    try:
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return float(data['price'])
    except Exception as e:
        print(f"Ошибка при получении курса {symbol}: {e}")
        return None

# Отдельные функции для каждой криптовалюты
async def get_ETH_in_USDT() -> Optional[float]:
    return await get_crypto_price('ETH')

async def get_USDT_in_USDT() -> Optional[float]:
    return 1.0  # USDT всегда равен 1 USDT

async def get_BNB_in_USDT() -> Optional[float]:
    return await get_crypto_price('BNB')

async def get_TON_in_USDT() -> Optional[float]:
    return await get_crypto_price('TON')

async def get_BTC_in_USDT() -> Optional[float]:
    return await get_crypto_price('BTC')

async def get_TRX_in_USDT() -> Optional[float]:
    return await get_crypto_price('TRX')

async def get_SOL_in_USDT() -> Optional[float]:
    return await get_crypto_price('SOL')

async def get_LTC_in_USDT() -> Optional[float]:
    return await get_crypto_price('LTC')

async def get_USDC_in_USDT() -> Optional[float]:
    return 1.0