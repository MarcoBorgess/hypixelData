from operator import getitem
from urllib import response
import requests
import json
import time

def getBazaar():
    response = requests.get('https://api.hypixel.net/skyblock/bazaar')
    response = json.loads(response.content)

    items = []

    for key in response['products'].keys():
        qq = response['products'][key]['quick_status']
        
        id  = response['products'][key]['product_id']
        sellPrice = qq['sellPrice']
        buyPrice = qq['buyPrice']
        sellVolume = qq['sellVolume']
        buyVolume = qq['buyVolume']
        sellMovingWeek = qq['sellMovingWeek']
        buyMovingWeek = qq['buyMovingWeek']
        sellOrders = qq['sellOrders']
        buyOrders = qq['buyOrders']
        updatedOn = response['lastUpdated']
        
        item = (id, sellPrice, buyPrice, sellVolume, buyVolume, sellMovingWeek, buyMovingWeek, sellOrders, buyOrders, updatedOn)
        items.append(item)
    
    return items

def getBins(ids):
    queryItems = [] 

    for item in ids:
        id = item[0]
        itemId = item[1]
        param = item[2]

        response = requests.get(f'https://sky.coflnet.com/api/item/price/{itemId}/bin{param}')
        
        if(response.status_code != requests.codes.ok):
            print(f'Failed to request {itemId}{param}')
            continue
        
        jsonData = json.loads(response.content)
        lowest = jsonData['lowest']
        secondLowest = jsonData['secondLowest']

        if(int(lowest) < 1):
            response = requests.get(f'https://sky.coflnet.com/api/item/price/{itemId}{param}')

            if(response.status_code != requests.codes.ok):
                print(f'Failed to request {itemId}{param}')
                continue

            jsonData = json.loads(response.content)
            lowest = jsonData['median']
            secondLowest = 0
        
        queryItem = (id, itemId, lowest, secondLowest, f'{int(time.time())}')
        queryItems.append(queryItem)
    
    return queryItems

def getItems():
    response = requests.get('https://api.hypixel.net/resources/skyblock/items')
    
    if(response.status_code != requests.codes.ok):
        print(f'Failed to request items list from hypixel')
        return

    jsonData = json.loads(response.content)
    allItems = jsonData['items']
    return allItems

def getItemFromCofl(itemId):
    response = requests.get(f'https://sky.coflnet.com/api/item/{itemId}/details')

    if(response.status_code != requests.codes.ok):
        print(f'Failed to request {itemId} from coflnet')
        return
    
    jsonData = json.loads(response.content)
    return jsonData