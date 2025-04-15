import json
from web3 import Account, HTTPProvider, Web3
from web3._utils import empty
import function.dataScript as dataScript
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for
import numpy as np 

app = Flask(__name__)
assetJson = {}
w3 = Web3(HTTPProvider('http://opgameplay.tplinkdns.com:8545'))
BIT_owner_address = None
USDT_Abi = {}
defaultAddress = None


# 0x Bf58 718F 95C8 b68f 90d5 92c3 43DD 676c 5fD2 f643
#    0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0042
# 0x095ea7b3000000000000000000000000bf58718f95c8b68f90d592c343dd676c5fd2f6430000000000000000000000000000000000000000000000000000000000000042

import function.assetGenerator as assetGenerator
import function.IPFS_simulate as IPFS_simulate
import function.contract as contract
@app.route('/gacha')
def gachaPage():
    generateReq = request.args.get('generateReq',None)
    targetAddress = request.args.get('targetAddress',None)
    metadata = None
    if generateReq and targetAddress:
        metadata = assetGenerator.FPS_Game_Skin()
        CID = IPFS_simulate.upload(metadata)
        assetsLastIndex = assetJson.get('assetsLastIndex', 0)
        assetJson['assetsLastIndex'] = assetsLastIndex + 1
        
        Asset_address = contract.asset_deploy(w3=w3, IPFS_CID=CID, assetID=assetJson['assetsLastIndex'], giveto_address=targetAddress, data=assetJson)
        assetJson['assets'][Asset_address] = {
            "asset_name": metadata.get('name', 'Null'),
            "address": Asset_address,
            "owner": targetAddress,
            "currencyAddress": assetJson[assetJson['settings']['TestMode']]['defaultAddress']
        }
        dataScript.save(assetJson)
    return render_template('gacha.html', metadata = metadata, previousTarget = targetAddress)

        
    
@app.route('/check_approve')
def check_aprove():
    assetAddress = request.args.get('assetAddress', None)
    buyerAddress  = request.args.get('buyer', None)
    price = request.args.get('price', None)
    result = {"approved": False,
              "allowance": 0}
    if assetAddress and buyerAddress and price:
        asset_safeAddress = w3.to_checksum_address(assetAddress)
        buyer_safeAddress = w3.to_checksum_address(buyerAddress)

        contract = w3.eth.contract(address=defaultAddress, abi=USDT_Abi)
        # print(contract.all_functions())
        allowance = contract.functions.allowance(buyer_safeAddress, asset_safeAddress).call()
        print(buyer_safeAddress)
        print(asset_safeAddress)
        print(allowance)
        if int(allowance) == int(price):
            result = {"approved": "True",
                      "allowance": allowance}
        if int(allowance) > int(price):
            result = {"approved": "False",
                      "allowance": allowance}
    
    return jsonify(result)

def get_average_of_all_month_by_events(events):
    M = []
    M_average = []
    for month in range(12):
        M.append([])
    now = datetime.now()
    for event in events:
        dateObject = contract.get_date_of_event(w3,event)
        if (dateObject.year == now.year and dateObject.month <= now.month) or (dateObject.year == (now.year-1) and dateObject.month > now.month):
            M[dateObject.month-1].append(event['args']['price_in_uToken'])
        else:
            break
    
    for month in range(12):
        # print(month)
        if len(M[month])>0:
            M_average.append(sum(M[month])/len(M[month]))
        else:
            M_average.append(0)
    return M_average
def rotate_list(lst, n):
    n = n % len(lst)  # 確保n在列表長度範圍內
    return lst[-n:] + lst[:-n]

from datetime import datetime
def generate_graph_by_event(events):
    now_month = datetime.now().month
    month_tranform = 12 - now_month
    width = 480
    height = 250
    # print(['args'][''])
    M_average = get_average_of_all_month_by_events(events)
    print(M_average)
    M_average = rotate_list(M_average, month_tranform)
    line = ''
    highest = 9
    while (highest<max(M_average)* 1.2):
        highest += 9

    
    for index, average in enumerate(M_average):
        line += f'{(width*(index)/12)+10}  {height-(height*average/highest)} '
        
    x_axis = ["1","2","3","4","5","6","7","8","9","10","11","12"]
    x_axis = rotate_list(x_axis, month_tranform)
    y_axis = []
    for i in range(9):
        y_axis.append(round(highest*(i)/9,1))
    
    graph = {
        "width" : "529px",
        "height": "286px",
        "lines" : [{"color":"5BCAC1","line":line}],
        "x_axis": x_axis,
        "y_axis": y_axis
    }
    return graph


@app.route('/detail')
def detail():
    query = request.args.get('address')
    if query:    
        data = assetJson['assets'][query]
        data['price'] = contract.get_price(w3, query)
        data['available'] = contract.get_available(w3, query)
        data['owner'] = contract.get_ownership(w3, query)
        data['currencyAddress'] = contract.getAssetCurrencyAddress(w3, query)
        print(data['currencyAddress'])
        data['symbol'] = contract.getSymbol(data['currencyAddress'])
        plaformFee = contract.getPlaformFee(w3, query)
        
        events = contract.get_event(w3, query)
        # print(events)
        graph = generate_graph_by_event(events)
        # graph = {
        #     "width" : "529px",
        #     "height": "286px",
        #     "lines" : [{"color":"5BCAC1","line":"0 0 450 250 "}],
        #     "x_axis": ["1","2","3","4","5","6","7","8","9","10","11","12"],
        #     "y_axis": ["0","10","20","30","40","50","60","70","80",]
        # }
        
        
        
        return render_template('detail.html', data=data, gas_price = w3.eth.gas_price/1000000000, plaformFee= plaformFee, graph = graph)
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
        address = result['address']
        
        result['price']  = str(contract.get_price(w3, address)) + ' (' + contract.getSymbol(contract.getAssetCurrencyAddress(w3, address)) + ')'
        result['available'] = contract.get_available(w3, address)
        result['owner'] = contract.get_ownership(w3, address)


        data['results'].append(result)
        
    return render_template('index.html', data=data)


if __name__ == '__main__':
    with open(r"contracts\USDT_Abi.json",'r') as f:
        USDT_Abi = json.load(f)
    assetJson = dataScript.load()
    BIT_owner_address = assetJson['init']['BIT_owner']
    defaultAddress = contract.getDefaultAddress(w3,assetJson)
    if defaultAddress:
        contract.bit_deploy(w3, data=assetJson)
        app.run(host='0.0.0.0',debug=True)