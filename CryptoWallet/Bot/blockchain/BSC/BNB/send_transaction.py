import asyncio
from web3 import AsyncWeb3


#Функция отправки BNB с одного кошелька на другой
async def send_bnb(sender_private_key, receiver_address, amount_in_bnb):
    bsc_node = "https://bsc-dataseed1.binance.org:443" #узел связи с блокчейном
    web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(bsc_node)) #создания web3 по данному узлу
    sender_account = await asyncio.to_thread(web3.eth.account.from_key, sender_private_key)#получаем аккаунт отправителя
    receiver_address = await asyncio.to_thread(web3.to_checksum_address, receiver_address)#преобразование в стандратный формат BSC
    nonce = await web3.eth.get_transaction_count(sender_account.address) #получаем число транзакций
    tx = {
        'nonce': nonce, #число транзакций отправителя
        'to': receiver_address, #адрес получателя
        'value': await asyncio.to_thread(web3.to_wei, amount_in_bnb, 'ether'), #количество токенов, которые мы хотим отправить - перевели их в Wei
        'gas': 21000, #лимит газа в Wei
        'gasPrice': await web3.eth.gas_price, #цена газа по рынку
    }
    signed_tx = await asyncio.to_thread(web3.eth.account.sign_transaction, tx, sender_private_key) #подписываем транзакцию
    tx_hash = await web3.eth.send_raw_transaction(signed_tx.rawTransaction) #отправляем транзакцию в блокчейн
    tx =await asyncio.to_thread(web3.to_hex, tx_hash)# преобразуем хеш в строку, чтобы перейти на сайт ABI
    return tx


