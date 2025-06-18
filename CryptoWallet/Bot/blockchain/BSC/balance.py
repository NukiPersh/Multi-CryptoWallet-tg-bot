from web3 import AsyncWeb3, Web3
import asyncio
from config_reader import config
import aiohttp


BSC_NODE = "https://bsc-dataseed1.binance.org:443"
web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(BSC_NODE))

ERC20_ABI = '[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]'

async def get_balance_in_BNB(address):
    balance = await web3.eth.get_balance(address)
    return balance / 10 ** 18

async def get_token_balance(address, token_address):
    token_address = Web3.to_checksum_address(token_address)
    token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
    balance = await token_contract.functions.balanceOf(address).call()
    return balance / 10 ** 18

async def get_balance_in_ETH(address):
    ETH_CONTRACT = "0x2170Ed0880ac9A755fd29B2688956BD959F933F8"
    return await get_token_balance(address, ETH_CONTRACT)

async def get_balance_in_USDT(address):
    USDT_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"
    return await get_token_balance(address, USDT_CONTRACT)

async def get_balance_in_TON(address):
    TON_CONTRACT = "0x76A797A59Ba2C17726896976B7B3747BfD1d220f"
    return await get_token_balance(address, TON_CONTRACT)

async def get_balance_in_BTC(address):
    BTC_CONTRACT = "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c"
    return await get_token_balance(address, BTC_CONTRACT)

async def get_balance_in_TRX(address):
    TRX_CONTRACT = "0xCE7de646e7208a4Ef112cb6ed5038FA6cC6b12e3"
    return await get_token_balance(address, TRX_CONTRACT)

async def get_balance_in_SOL(address):
    SOL_CONTRACT = "0x570A5D26f7765Ecb712C0924E4De545B89fD43dF"
    return await get_token_balance(address, SOL_CONTRACT)

async def get_balance_in_LTC(address):
    LTC_CONTRACT = "0x4338665CBB7B2485A8855A139b75D5e34AB0DB94"
    return await get_token_balance(address, LTC_CONTRACT)

async def get_balance_in_USDC(address):
    USDC_CONTRACT = "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"
    return await get_token_balance(address, USDC_CONTRACT)







async def get_all_balances(address):
    contracts = {
        "ETH": "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
        "USDT": "0x55d398326f99059fF775485246999027B3197955",
        "TON": "0x76A797A59Ba2C17726896976B7B3747BfD1d220f",
        "BTC": "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
        "TRX": "0xCE7de646e7208a4Ef112cb6ed5038FA6cC6b12e3",
        "SOL": "0x570A5D26f7765Ecb712C0924E4De545B89fD43dF",
        "LTC": "0x4338665CBB7B2485A8855A139b75D5e34AB0DB94",
        "USDC": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"
    }
    tasks = [get_token_balance(address, token) for token in contracts.values()]
    results = await asyncio.gather(*tasks)

    formatted_results = {k: f"{v:.7f}" for k, v in zip(contracts.keys(), results)}

    return formatted_results



