import json
from web3 import Web3


#0x095ea7b3000000000000000000000000Bf58718F95C8b68f90d592c343DD676c5fD2f643b4c3000000000000000000000000000000000000000000000000000000000000
#0x095ea7b3000000000000000000000000Bf58718F95C8b68f90d592c343DD676c5fD2f643b4c3000000000000000000000000000000000000000000000000000000000000

# 連接到以太坊節點（可以使用Infura等節點）
w3 = Web3(Web3.HTTPProvider('http://172.28.224.1:8545'))

# 以太坊發送者地址（需要有足夠的以太幣用於交易手續費）
sender_address = '0x7491058489b5FF454a931d0172C6d729D7587bb1'
private_key = '0x89d639531dc7d4bc27acb5b7bc0900bfd1a529b40ac02bcb493c67cb16e595c7'

# 接收者地址
receiver_address = '0x271D0a64BaC8870897eF54d32D6B24e88493898F'

def test_gas_est():
    GameAssetAbi = {}
    with open("GameAssetAbi.json",'r') as f:
        GameAssetAbi = json.load(f)
        
    asset_address = "0xBf58718F95C8b68f90d592c343DD676c5fD2f643"
    contract = w3.eth.contract(address=asset_address, abi=GameAssetAbi)
    
    # 
    Function = contract.functions.Purchase()
    
    tx = {'from':sender_address, 'gasPrice': w3.eth.gas_price}
    
    # txn = Function.transact()
    Gas_Est = Function.estimate_gas(transaction=tx)
    print(Gas_Est)
    
    
if __name__ == '__main__':
    test_gas_est()