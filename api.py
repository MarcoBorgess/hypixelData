import requests
import json
import time


# Request data from hypixel bazaar api and return every item in the bazaar
def getBazaar():
    response = requests.get('https://api.hypixel.net/skyblock/bazaar')
    
    if(response.status_code != requests.codes.ok):
        print(f'⚠️ Failed to request bazaar from hypixel')
        return
    
    response = json.loads(response.content)

    items = []

    for key in response['products'].keys():
        qq = response['products'][key]['quick_status']
        
        idHypixel  = response['products'][key]['product_id']
        sellPrice = qq['sellPrice']
        buyPrice = qq['buyPrice']
        sellVolume = qq['sellVolume']
        buyVolume = qq['buyVolume']
        sellMovingWeek = qq['sellMovingWeek']
        buyMovingWeek = qq['buyMovingWeek']
        sellOrders = qq['sellOrders']
        buyOrders = qq['buyOrders']
        updatedOn = response['lastUpdated']
        
        item = (idHypixel, sellPrice, buyPrice, sellVolume, buyVolume, sellMovingWeek, buyMovingWeek, sellOrders, buyOrders, updatedOn)
        items.append(item)
    
    return items

def getBins(ids):
    print('✅ Getting bins...')
    queryItems = []
    
    for id in ids:
        idHypixel = id[0]
        itemId = idHypixel
        param = ''

        if '?' in idHypixel:
            param = '?'
            itemId = idHypixel.split('?')[0]
            param += idHypixel.split('?')[1]
    
        response = requests.get(f'https://sky.coflnet.com/api/item/price/{itemId}/bin{param}')
        
        if(response.status_code != requests.codes.ok):
            print(f'⚠️ Failed to request {itemId}{param}')
            continue
    
        jsonData = json.loads(response.content)
        lowest = jsonData['lowest']
        secondLowest = jsonData['secondLowest']
        
        queryItem = (idHypixel, lowest, secondLowest, f'{int(time.time())}')

        if(int(lowest) < 1):
            response = requests.get(f'https://sky.coflnet.com/api/item/price/{itemId}{param}')

            if(response.status_code != requests.codes.ok):
                print(f'Failed to request {itemId}{param}')
                continue

            jsonData = json.loads(response.content)
            lowest = jsonData['median']
            secondLowest = 0
            
            queryItem = (idHypixel, lowest, secondLowest, f'{int(time.time())}')
            
        queryItems.append(queryItem)
    
    return queryItems

# Request all items from hypixel and return them
def getItems():
    response = requests.get('https://api.hypixel.net/resources/skyblock/items')
    
    if(response.status_code != requests.codes.ok):
        print(f'⚠️ Failed to request items list from hypixel')
        return

    jsonData = json.loads(response.content)
    allItems = jsonData['items']
    
    return allItems

# Request item by id from coflnet and return it
def getItemFromCofl(idHypixel):
    itemId = idHypixel
    param = ''
    
    if '?' in idHypixel:
        param = '?'
        itemId = idHypixel.split('?')[0]
        param += idHypixel.split('?')[1]
    
    response = requests.get(f'https://sky.coflnet.com/api/item/{itemId}/details{param}')

    if(response.status_code != requests.codes.ok):
        print(f'⚠️ Failed to request {idHypixel} from coflnet')
        return
    
    jsonData = json.loads(response.content)
    return jsonData