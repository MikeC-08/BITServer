import json

def search_asset(jsonData, asset_name=None, address=None, limit=20):
    """
    搜尋指定名稱或地址的資產。

    :param assets: JSON格式的資產列表
    :param asset_name: 資產名稱
    :param address: 資產地址
    :return: 滿足搜尋條件的資產列表
    """
    results = []

    for item in jsonData['assets'].values():
       
        if (asset_name is None or asset_name.lower() in item['asset_name'].lower()) and \
           (address is None or address.lower() in item['address'].lower()):
            results.append(item)
            
            
        if len(results) >= limit:
            break
    return results

def load():
    with open(r"data.json",'r' , encoding='utf-8') as f:
        return json.load(f)

def save(jsonData):
    with open(r"data.json",'w', encoding='utf-8') as f:
        json.dump(jsonData, f, ensure_ascii=False, indent=4)