import requests
import json

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