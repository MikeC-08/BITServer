import json
from web3 import Account, HTTPProvider, Web3
from web3._utils import empty
import function.dataScript as dataScript
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for
import numpy as np 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 為安全起見，請使用一個強密鑰
assetJson = {}
w3 = Web3(HTTPProvider('http://opgameplay.tplinkdns.com:8545'))
GameAssetAbi = {}
USDC_Abi = {}
USDC_ADDRESS = '0xB4AcC2D7E94Eb1188Fd91c5b5F0B3aD06A140541'

@app.route('/approve_transaction')
def approve_transaction():
    
    buyer = request.args.get('address')
    price = 10
    asset = request.args.get('asset')
    print(buyer)

    buyer_safeAddress = Web3.to_checksum_address(buyer)
    
    contract = w3.eth.contract(address=USDC_ADDRESS, abi=USDC_Abi)
    tx_for_estimate_gas = {'from':buyer_safeAddress, 'gasPrice': w3.eth.gas_price}
    
    # print(contract.functions.approve(asset,price).argument_types)
    estimate_gas = contract.functions.approve(asset,price).estimate_gas(tx_for_estimate_gas)
    transaction = {
        'gas': estimate_gas
    }
    return jsonify(transaction)
# 0x Bf58 718F 95C8 b68f 90d5 92c3 43DD 676c 5fD2 f643
#    0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0042
# 0x095ea7b3000000000000000000000000bf58718f95c8b68f90d592c343dd676c5fd2f6430000000000000000000000000000000000000000000000000000000000000042


@app.route('/transaction')
def transaction():
    buyer = request.args.get('address')
    price = request.args.get('price')
    asset = request.args.get('asset')

    contract = w3.eth.contract(address=asset, abi=GameAssetAbi)
    
    tx_for_estimate_gas = {'from':'0x7491058489b5FF454a931d0172C6d729D7587bb1', 'gasPrice': w3.eth.gas_price}
    estimate_gas = contract.functions.Purchase().estimate_gas(tx_for_estimate_gas)
    
    transaction = {
        'from': buyer,
        'gasPrice': w3.eth.gas_price,
        'gas': estimate_gas
    }
    return jsonify(transaction)



@app.route('/detail')
def detail():
    query = request.args.get('address')
    if query:
        data = assetJson['assets'][query]
        
        
        return render_template('detail.html', data=data, gas_price = w3.eth.gas_price/1000000000)
    else:
        return redirect('/')

@app.route('/')
def home():
    query = request.args.get('query')
    method = request.args.get('method')



    if not query:
        query = ""
    if not method:
        method = "byName"
        
        
    if method=="byName":
        results = dataScript.search_asset(assetJson, asset_name=query)
    if method=="byAddress":
        results = dataScript.search_asset(assetJson, address=query)
    data = {
        "results":[]
    }
    for result in results:
        #{'asset_name': '測試一下', 'owner': 'CHCH', 'price': 10}
        data['results'].append(result)
    print(results)

        
    return render_template('index.html', data=data)


if __name__ == '__main__':
    with open("GameAssetAbi.json",'r') as f:
        GameAssetAbi = json.load(f)
    with open("USDC_Abi.json",'r') as f:
        USDC_Abi = json.load(f)
        
    assetJson = dataScript.load()
    app.run(debug=True, host='0.0.0.0')