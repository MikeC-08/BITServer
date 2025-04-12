import os
from solcx import compile_standard, install_solc
import json
from dotenv import load_dotenv
load_dotenv()
import web3
install_solc('0.8.29')

def compile(name):
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
        solc_version="0.8.29",
    )

    with open(fr".\contracts\compiled_{name}.json","w") as file:
        json.dump(compiled_sol,file)

def bit_deploy(w3, chain_id, BIT_owner_address):
    compile("BIT")
    with open('data.json', 'r') as f:
        data = json.load(f)
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
    
    nonce = w3.eth.get_transaction_count(BIT_owner_address)
    
    transaction = BIT.constructor().build_transaction(
                    {
                        "chainId": chain_id,
                        "gasPrice": w3.eth.gas_price,
                        "from": BIT_owner_address,
                        "nonce": nonce
                    }
                )
    
    estimate_gas = w3.eth.estimate_gas(transaction)
    print(f"* Estimate Gas is {estimate_gas} Units. Gas Price is {w3.eth.gas_price}")
    print(f"* Estimate Gas Fee is {estimate_gas * w3.eth.gas_price} Wei / {estimate_gas * w3.eth.gas_price * 0.000000001} Gwei / {estimate_gas * w3.eth.gas_price * 0.000000001 * 0.000000001} Ether")
    Continue = input("> Would you like to continue the transaction? <yes> / <no> :")
    if Continue != 'yes':
        return
    
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


    
def asset_deploy(w3, chain_id, BIT_owner_address, IPFS_CID, assetID, giveto_address):
    bit_deploy(chain_id, BIT_owner_address)
    compile("GameAsset")
    compiled_sol_path = fr".\contracts\compiled_GameAsset.json"
    with open('data.json', 'r') as f:
        data = json.load(f)
    if data['BIT_address'] == '':
        print('BIT_address cannot be empty')
        return
    
    with open(compiled_sol_path,"r") as file:
        compiled_sol = json.load(file)
        
    bytecode = compiled_sol["contracts"][".\contracts\GameAsset.sol"]["GameAsset"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"][".\contracts\GameAsset.sol"]["GameAsset"]["abi"]
    GameAsset = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    nonce = w3.eth.get_transaction_count(BIT_owner_address)
    
    transaction = GameAsset.constructor(data['BIT_address'], str(IPFS_CID), giveto_address).build_transaction(
                    {
                        "chainId": chain_id,
                        "gasPrice": w3.eth.gas_price,
                        "from": BIT_owner_address,
                        "nonce": nonce
                    }
                )
    

    
    
    estimate_gas = w3.eth.estimate_gas(transaction)
    checksum_address = w3.to_checksum_address(BIT_owner_address)
    balance = w3.eth.get_balance(checksum_address)
    print(f"* Account Balance: {balance}")
    print(f"* Estimate Gas is {estimate_gas + 32000*1.2} Units. Gas Price is {w3.eth.gas_price}")
    print(f"* Estimate Gas Fee is {(estimate_gas + 32000) * w3.eth.gas_price*1.2} Wei / {(estimate_gas + 32000) * w3.eth.gas_price * 0.000000001*1.2} Gwei / {(estimate_gas + 32000) * w3.eth.gas_price * 0.000000001 * 0.000000001*1.2} Ether")
    Continue = input("> Would you like to continue the transaction? <yes> / <no> :")
    if Continue != 'yes':
        return
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
    
def get_ownership(w3, address):
    abi = get_asset_abi()
    Asset_Contract = w3.eth.contract(address=address, abi=abi)
    return Asset_Contract.functions.owner().call()
    
def get_price(w3, address):
    abi = get_asset_abi()
    Asset_Contract = w3.eth.contract(address=address, abi=abi)
    return Asset_Contract.functions.price_in_uUSDC().call()

def get_available(w3, address):
    abi = get_asset_abi()
    Asset_Contract = w3.eth.contract(address=address, abi=abi)
    return Asset_Contract.functions.isList().call()


    
if __name__ == '__main__':
    chain_id = 31337 # Hardhat
    BIT_owner_address = '0x271D0a64BaC8870897eF54d32D6B24e88493898F'
    w3 = web3.Web3(web3.Web3.HTTPProvider('http://opgameplay.tplinkdns.com:8545'))
    IPFS_CID = 'test'
    # asset_deploy(chain_id, BIT_owner_address, IPFS_CID, 9999, '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266')
    
    print(get_price(w3, '0xf68b5B3E09d61eBe2C0f683817e19D3a1a0cE055')) # should be 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
