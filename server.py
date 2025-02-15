import json
from web3 import Account, HTTPProvider, Web3
from web3._utils import empty
import function.dataScript as dataScript
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for
import numpy as np 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 為安全起見，請使用一個強密鑰
assetJson = {}
w3 = Web3(HTTPProvider('HTTP://127.0.0.1:7545'))
GameAssetAbi = {}
@app.route('/transaction')
def transaction():
    buyer = request.args.get('address')
    price = request.args.get('price')
    asset = request.args.get('asset')

    contract = w3.eth.contract(address=asset, abi=GameAssetAbi)
    eg = contract.functions.Purchase().estimate_gas()
    print(eg)   
    
    
    # tx = contract.functions.Purchase().buildTransaction({
        
    # 'nonce': w3.eth.get_transaction_count(buyer),
    # 'from': buyer,
    # 'gasPrice': w3.eth.gas_price,
    # 'gas': '0'
    # })
    # eg = w3.eth.estimate_gas()
    # tx.update({'gas': eg})
    transaction = {
        'from': buyer,
        'gasPrice': w3.eth.gas_price,
        'gas': eg
    }
    return jsonify(transaction)

@app.route('/detail')
def detail():
    query = request.args.get('address')
    if query:
        data = assetJson['assets'][query]
        
        
        return render_template('detail.html', data=data)
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
    assetJson = dataScript.load()
    app.run(debug=True)