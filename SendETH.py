from web3 import Web3

# 連接到以太坊節點（可以使用Infura等節點）
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3 = Web3(Web3.HTTPProvider('http://opgameplay.tplinkdns.com:8545'))

# 以太坊發送者地址（需要有足夠的以太幣用於交易手續費）
sender_address = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'



# 接收者地址
receiver_address1 = '0x271D0a64BaC8870897eF54d32D6B24e88493898F'
receiver_address2= '0xaaA9ea39E21Cfb146341AD098C0D74B07eb59DBC'
# 以太坊交易參數
transaction1 = {
    'to': receiver_address1,
    'value': w3.to_wei(1, 'ether'),
    'gas': 2000000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': w3.eth.get_transaction_count(sender_address),
}
transaction2 = {
    'to': receiver_address2,
    'value': w3.to_wei(1, 'ether'), 
    'gas': 2000000,
    'gasPrice': w3.to_wei('50', 'gwei'), 
    'nonce': w3.eth.get_transaction_count(sender_address)+1,
}
# 簽署交易
signed_txn1 = w3.eth.account.sign_transaction(transaction1, private_key)
signed_txn2 = w3.eth.account.sign_transaction(transaction2, private_key)

# 發送交易
tx_hash1 = w3.eth.send_raw_transaction(signed_txn1.raw_transaction)
tx_hash2 = w3.eth.send_raw_transaction(signed_txn2.raw_transaction)

print('交易已發送，交易哈希：', w3.to_hex(tx_hash1))
print('交易已發送，交易哈希：', w3.to_hex(tx_hash2))