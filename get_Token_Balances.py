import function.contract as contract
import web3
import json
import sys

if __name__ == '__main__':
    address = sys.argv[1]
    chain_id = 31337 # Hardhat
    
    # w3 = web3.Web3(web3.Web3.HTTPProvider('https://eth.llamarpc.com')) # mainnet
    w3 = web3.Web3(web3.Web3.HTTPProvider('http://127.0.0.1:8545'))
    with open(r"data.json",'r' , encoding='utf-8') as f:
        data =  json.load(f)

    print(contract.get_USDT_test_balance(w3, address, data)) # should be 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
    