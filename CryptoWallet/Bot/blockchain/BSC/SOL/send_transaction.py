import asyncio
from web3 import AsyncWeb3


#Функция отправки SOL с одного кошелька на другой
async def send_token_sol(sender_private_key, receiver_address, amount_in_token):
    bsc_node = "https://bsc-dataseed1.binance.org:443" #узел связи с блокчейном
    web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(bsc_node)) #создания web3 по данному узлу
    contract_token = "0x570A5D26f7765Ecb712C0924E4De545B89fD43dF" #контракт соланы
    contract_abi = [
        {
            "constant": False,
            "inputs": [
                {"name": "_to", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        }
    ]
    sender_account = await asyncio.to_thread(web3.eth.account.from_key, sender_private_key)
    receiver_address = await asyncio.to_thread(web3.to_checksum_address, receiver_address)
    contract_address = await asyncio.to_thread(web3.to_checksum_address, contract_token)
    contract =web3.eth.contract(address=contract_address, abi=contract_abi)
    nonce = await web3.eth.get_transaction_count(sender_account.address) 
    amount_in_wei = await asyncio.to_thread(web3.to_wei, amount_in_token, 'ether')
    tx = {
        'chainId': 56,
        'from': sender_account.address,
        'to': contract_address,
        'gas': 100000,  
        'gasPrice': await web3.eth.gas_price,
        'nonce': nonce,
        'data': contract.encodeABI(
            fn_name='transfer',
            args=[receiver_address, amount_in_wei]
        ),
        'value': 0  
    }
    signed_tx = await asyncio.to_thread(web3.eth.account.sign_transaction, tx, sender_private_key) #подписываем транзакцию
    tx_hash = await web3.eth.send_raw_transaction(signed_tx.rawTransaction) #отправляем транзакцию в блокчейн
    tx =await asyncio.to_thread(web3.to_hex, tx_hash)# преобразуем хеш в строку, чтобы перейти на сайт ABI
    return tx


