import os
from solcx import compile_standard, install_solc
import json
from dotenv import load_dotenv
load_dotenv()
import web3


def compile(name, version):
    install_solc(version)
    path = fr".\contracts\{name}.sol"
    with open(path,"r") as file:
        sol_file = file.read()
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {path: {"content": sol_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version=version,
    )

    with open(fr".\contracts\compiled_{name}.json","w") as file:
        json.dump(compiled_sol,file)


def getSymbol(currency_address):
    with open('CurrencySymbol.json','r') as f:
        data =  json.load(f)
    if currency_address in data.keys():
        return data[currency_address]
    else:
        return "Unknown Token"
    
def getAssetCurrencyAddress(w3, asset_address):
    abi = get_asset_abi()
    assetContract = w3.eth.contract(address=asset_address, abi=abi)
    return assetContract.functions.token_address().call()
    
        
def getDefaultAddress(w3, data):
    chain_id = w3.eth.chain_id
    defaultAddress = data[data['settings']['TestMode']]['defaultAddress']
    with open(r'.\contracts\USDT_Abi.json','r') as f:
        abi = json.load(f)
    try:
        CurrencyContract = w3.eth.contract(address=defaultAddress, abi=abi)
        CurrencyContract.functions.totalSupply().call()
        return defaultAddress
    except:
        defaultAddress = None
        data[data['settings']['TestMode']]['defaultAddress'] = 'Error'
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print('* The Default Address seems not correct')
        
    if data['settings']['TestMode'] == 'test':
        Continue  = input('> Delopy USDT(test) for BIT? <yes>/<no>: ')
        if Continue != 'yes':
            return None
        else:
            compile("USDT_for_test", "0.4.26")
            compiled_sol_path = fr".\contracts\compiled_USDT_for_test.json"
            with open(compiled_sol_path,"r") as file:
                compiled_sol = json.load(file)
                bytecode = compiled_sol["contracts"][r".\contracts\USDT_for_test.sol"]["TetherToken"]["evm"]["bytecode"]["object"]
                abi = compiled_sol["contracts"][r".\contracts\USDT_for_test.sol"]["TetherToken"]["abi"]
                USDT_Test = w3.eth.contract(abi=abi, bytecode=bytecode)
                nonce = w3.eth.get_transaction_count(data['init']['BIT_owner'])
                
                transaction = USDT_Test.constructor(100000000000, "Tether USD", "USDT", 6).build_transaction(
                                {
                                    "chainId": chain_id,
                                    "gasPrice": w3.eth.gas_price,
                                    "from": data['init']['BIT_owner'],
                                    "nonce": nonce
                                }
                            )
                estimate_gas = w3.eth.estimate_gas(transaction)
                checksum_address = w3.to_checksum_address(data['init']['BIT_owner'])
                balance = w3.eth.get_balance(checksum_address)
                if balance <= (estimate_gas * w3.eth.gas_price)*1.2:
                    print("Balance may not insufficient to pay.")
                    return False
                signed_txn = w3.eth.account.sign_transaction(transaction, private_key= os.getenv("PRIVATE_KEY"))
                print("Deploying Contract…")
                tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
                print("Waiting for transaction to finish...")
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                Asset_address = tx_receipt.contractAddress
                print(f"* USDT for test deployed at address: {Asset_address}")
                with open('CurrencySymbol.json','r') as f:
                    CurrencySymbol =  json.load(f)
                CurrencySymbol[Asset_address] = data['test']['defaultSymbol']
                with open('CurrencySymbol.json','w') as f:
                    json.dump(CurrencySymbol,f,indent=4)
                data['test']['defaultAddress']=Asset_address
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
                defaultAddress = Asset_address
                return defaultAddress
                
    else:
        return defaultAddress

def USDT_test_Give(w3, data, target_address):
    defaultAddress = data[data['settings']['TestMode']]['USDT_test']
    with open(r'.\contracts\USDT_Abi.json','r') as f:
        abi = json.load(f)
    nonce = w3.eth.get_transaction_count(data['init']['BIT_owner'])
    CurrencyContract = w3.eth.contract(address=defaultAddress, abi=abi)
    transaction = CurrencyContract.functions.give(target_address, 10000000).build_transaction(
                                        {
                                            "chainId": chain_id,
                                            "gasPrice": w3.eth.gas_price,
                                            "from": data['init']['BIT_owner'],
                                            "nonce": nonce
                                        }
                                    )
    estimate_gas = w3.eth.estimate_gas(transaction)
    checksum_address = w3.to_checksum_address(data['init']['BIT_owner'])
    balance = w3.eth.get_balance(checksum_address)
    if balance <= (estimate_gas * w3.eth.gas_price)*1.2:
        print("Balance may not insufficient to pay.")
        return False
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= os.getenv("PRIVATE_KEY"))
    print("Deploying Contract…")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"* Given |tx_receipt:{tx_receipt}")         
    return
    
                    
def bit_deploy(w3, data):
    chain_id = w3.eth.chain_id
    compile("BIT","0.8.29")
    if data['BIT_address'] != '':
        return
    print('* Detect BIT is not deployed.')
    
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        print("Private Key is needed for deploying the BIT")
    
    
    
    Continue = input("> Would you like to deployed the BIT Mother Contract? <yes> / <no> : ")
    if Continue != 'yes':
        return
    compiled_sol_path = fr".\contracts\compiled_BIT.json"
    
    with open(compiled_sol_path,"r") as file:
        compiled_sol = json.load(file)
        
    bytecode = compiled_sol["contracts"][".\contracts\BIT.sol"]["BIT"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"][".\contracts\BIT.sol"]["BIT"]["abi"]
    BIT = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    nonce = w3.eth.get_transaction_count(data['init']['BIT_owner'])
    
    transaction = BIT.constructor().build_transaction(
                    {
                        "chainId": chain_id,
                        "gasPrice": w3.eth.gas_price,
                        "from": data['init']['BIT_owner'],
                        "nonce": nonce
                    }
                )
    
    # estimate_gas = w3.eth.estimate_gas(transaction)
    # print(f"* Estimate Gas is {estimate_gas} Units. Gas Price is {w3.eth.gas_price}")
    # print(f"* Estimate Gas Fee is {estimate_gas * w3.eth.gas_price} Wei / {estimate_gas * w3.eth.gas_price * 0.000000001} Gwei / {estimate_gas * w3.eth.gas_price * 0.000000001 * 0.000000001} Ether")
    # Continue = input("> Would you like to continue the transaction? <yes> / <no> :")
    # if Continue != 'yes':
    #     return
    
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= os.getenv("PRIVATE_KEY"))
    print("Deploying Contract…")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    BIT_address = tx_receipt.contractAddress
    print(f"* BIT deployed at address: {BIT_address}")
    data['BIT_address'] = str(BIT_address)
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


    
def asset_deploy(w3, IPFS_CID, assetID, giveto_address, data):
    compile("GameAsset","0.8.29")
    compiled_sol_path = fr".\contracts\compiled_GameAsset.json"

    if data['BIT_address'] == '':
        print('BIT_address cannot be empty')
        return
    
    with open(compiled_sol_path,"r") as file:
        compiled_sol = json.load(file)
        
    bytecode = compiled_sol["contracts"][".\contracts\GameAsset.sol"]["GameAsset"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"][".\contracts\GameAsset.sol"]["GameAsset"]["abi"]
    GameAsset = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    nonce = w3.eth.get_transaction_count(data['init']['BIT_owner'])
    
    transaction = GameAsset.constructor(data['BIT_address'], str(IPFS_CID), giveto_address, data[data['settings']['TestMode']]['defaultAddress'], int(data['settings']['platform_fee_wei'])).build_transaction(
                    {
                        "chainId": w3.eth.chain_id,
                        "gasPrice": w3.eth.gas_price,
                        "from": data['init']['BIT_owner'],
                        "nonce": nonce
                    }
                )
    

    
    
    estimate_gas = w3.eth.estimate_gas(transaction)
    checksum_address = w3.to_checksum_address(data['init']['BIT_owner'])
    balance = w3.eth.get_balance(checksum_address)
    if balance <= ((estimate_gas + 32000) * w3.eth.gas_price)*1.2:
        print("Balance may not insufficient to pay.")
    
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key= os.getenv("PRIVATE_KEY"))
    print("Deploying Contract…")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    Asset_address = tx_receipt.contractAddress
    print(f"* GameAsset deployed at address: {Asset_address}")
    
    BIT_Address = data['BIT_address']
    BIT_compiled_sol_path = fr".\contracts\compiled_BIT.json"
    with open(BIT_compiled_sol_path,"r") as file:
        BIT_compiled_sol_path = json.load(file)
    # BIT_bytecode = BIT_compiled_sol_path["contracts"][".\contracts\BIT.sol"]["BIT"]["evm"]["bytecode"]["object"]
    print(f"* Interacting with BIT...")
    BIT_abi = BIT_compiled_sol_path["contracts"][".\contracts\BIT.sol"]["BIT"]["abi"]
    BIT_Contract = w3.eth.contract(address=BIT_Address, abi=BIT_abi)
    BIT_Contract.functions.addNewSubItemAddrWithID(assetID, Asset_address).call()
    print(f"* New assets have been added.")
    return Asset_address
    
def get_asset_abi():
    compiled_sol_path = fr".\contracts\compiled_GameAsset.json"
    with open(compiled_sol_path,"r") as file:
        compiled_sol = json.load(file)
    return compiled_sol["contracts"][".\contracts\GameAsset.sol"]["GameAsset"]["abi"]
    
def getPlaformFee(w3, address):
    checksum_address = w3.to_checksum_address(address)
    abi = get_asset_abi()
    Asset_Contract = w3.eth.contract(address=checksum_address, abi=abi)
    return Asset_Contract.functions.platform_fee_eth().call()


def get_ownership(w3, address):
    checksum_address = w3.to_checksum_address(address)
    abi = get_asset_abi()
    Asset_Contract = w3.eth.contract(address=checksum_address, abi=abi)
    return Asset_Contract.functions.owner().call()
    
def get_price(w3, address):
    abi = get_asset_abi()
    Asset_Contract = w3.eth.contract(address=address, abi=abi)
    return Asset_Contract.functions.price_in_uToken().call()

def get_available(w3, address):
    abi = get_asset_abi()
    Asset_Contract = w3.eth.contract(address=address, abi=abi)
    return Asset_Contract.functions.isList().call()

def get_USDT_test_balance(w3, address:str, data):
    
    checksum_address = w3.to_checksum_address(address)
    compiled_sol_path = fr".\contracts\compiled_USDT_for_test.json"
    with open(compiled_sol_path,"r") as file:
        compiled_sol = json.load(file)
    abi = compiled_sol["contracts"][r".\contracts\USDT_for_test.sol"]["BasicToken"]["abi"]
    Asset_Contract = w3.eth.contract(address=data[data['settings']['TestMode']]['defaultAddress'], abi=abi)
    

    return Asset_Contract.functions.balanceOf(checksum_address).call()


def get_date_of_event(w3,event):
    block = w3.eth.get_block(event['blockHash'])
    # print(block)
    timestamp = block['timestamp']
    # print(timestamp)
    dt_object = datetime.fromtimestamp(timestamp)
    # print("日期時間:", dt_object)
    return dt_object
    
    
from datetime import datetime
def get_event(w3, address):
    abi = get_asset_abi()
    Asset_Contract = w3.eth.contract(address=address, abi=abi)
    # block = w3.eth.block_number

    events = Asset_Contract.events.OwnershipTransferred().get_logs(from_block=0)

    

    return events
if __name__ == '__main__':
    chain_id = 31337 # Hardhat
    
    # w3 = web3.Web3(web3.Web3.HTTPProvider('https://eth.llamarpc.com')) # mainnet
    w3 = web3.Web3(web3.Web3.HTTPProvider('http://opgameplay.tplinkdns.com:8545'))
    with open(r"data.json",'r' , encoding='utf-8') as f:
        data =  json.load(f)
    IPFS_CID = 'test'
    # asset_deploy(chain_id, BIT_owner_address, IPFS_CID, 9999, '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266')
    
    events=get_event(w3,'0x08676949512862791993E0733FFfd4F7DfF3C673')
    print(events)
    # graph = generate_graph_by_event(events)
        
        
    
    
    # print(get_USDT_test_balance(w3, '0x271d0a64bac8870897ef54d32d6b24e88493898f', data)) # should be 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
    # getdefaultAddress(w3,'0x271D0a64BaC8870897eF54d32D6B24e88493898F')
