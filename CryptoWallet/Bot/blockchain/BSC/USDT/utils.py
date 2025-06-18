import aiohttp
import asyncio

from web3 import AsyncWeb3
from eth_account import Account
from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum

from database import database_func

from Cryptography import cryptography_pkeys

#Функция Генерация сид-фразы
async def get_generate_bnb_seed_phrase():
    #получаем сид фразу длины 12:
    seed_phrase = await asyncio.to_thread(Bip39MnemonicGenerator().FromWordsNumber, Bip39WordsNum.WORDS_NUM_12)
    return seed_phrase

# Создание нового кошелька и получение приватного ключа с адрессом
async def get_create_wallet_from_mnemonic(seed_phrase):
    await asyncio.to_thread(Account.enable_unaudited_hdwallet_features)#получаем доступ к особым функциям (не прошли аудит)
    private_key =await asyncio.to_thread(lambda: Account.from_mnemonic(seed_phrase)._private_key.hex()) #получаем приватный ключ из сид фразы
    address = await asyncio.to_thread(lambda: Account.from_key(private_key).address) #полуачем адрес из приватного ключа
    return private_key, address

#получение адреса из приватного ключа
async def get_address_from_pk(private_key):
    await asyncio.to_thread(Account.enable_unaudited_hdwallet_features)#получаем доступ к особым функциям (не прошли аудит)
    address = await asyncio.to_thread(lambda: Account.from_key(private_key).address) #получаем адрес из приватного ключа
    return address

#проверка что это валидная сид фраза
async def check_on_seed_phrase(seed_phrase):
    await asyncio.to_thread(Account.enable_unaudited_hdwallet_features)#получаем доступ к особым функциям (не прошли аудит)
    #пытаемся из полученной строки получить приватный ключ, если успешно - то это сид фраза, иначе не сид фраза
    try:
        await asyncio.to_thread(lambda: Account.from_mnemonic(seed_phrase)._private_key.hex())
        return True
    except:
        return False
    
#проверка что это валидный приватный ключ
async def check_on_privacykey(private_key):
    await asyncio.to_thread(Account.enable_unaudited_hdwallet_features)#получаем доступ к особым функциям (не прошли аудит)
    #пытаемся из приватного ключа получить адрес, если успешно - то это приватный ключ, иначе не приватный ключ
    try:
        await get_address_from_pk(private_key)
        return True
    except:
        return False

#проверка что это пароль
async def check_password_for_pk(telegram_id, password):
    encrypted_pk = await database_func.get_privacy_key(telegram_id) #достаем зашифрованный приватный ключ из бд
    decrypted_pk = await cryptography_pkeys.decrypt_private_key(encrypted_pk, password)#расшифруем приватный ключ
    if decrypted_pk == None:# если в результате расшифровки получили None, то значит пароль не подходит
        return False
    address_from_decrypted_dk = await get_address_from_pk(decrypted_pk)# получаем адрес из приватного ключа
    address_from_db = await database_func.get_address(telegram_id)# получаем адрес из бд
    if address_from_decrypted_dk == address_from_db: # если совпало, то наш пароль подходит, иначе пароль не верный
        return True
    else:
        return False

#проверка что это адресс
async def check_address_for_transfer(address):
    #если смогли получить баланс кошелька, то такой кошелек есть, иначе нет
    try:
        await get_balance_in_USDT(address)
        return True
    except:
        return False

 # Получение средней цены газа из блокчейна (в Wei)
async def get_gas_price():
    bsc_node = "https://bsc-dataseed1.binance.org:443"
    web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(bsc_node))
    gas_price = await web3.eth.gas_price #получение цены за газ
    return (21000 * gas_price)/10**18 #перевод в понятную для транзакции СИ

# Получение баланса USDT aSync
async def get_balance_in_USDT(address):
    bsc_node = "https://bsc-dataseed1.binance.org:443"
    web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(bsc_node))
    balance = await web3.eth.get_balance(address) #получаем баланс кошелька
    return balance/10**18  #возвращаем баланс в USDT


#Получить курс USDT USDT async
async def get_USDT_in_USDT():
    try:
        url = 'https://api.binance.com/api/v3/ticker/price?symbol=USDTUSDT' #ссылка для запроса
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                usdt_to_usdt = float(data['price'])
                return usdt_to_usdt #возвращаем значение цены 
    except Exception as e:
        print(f"Произошла ошибка при получении курса USDT в USDT: {e}")
