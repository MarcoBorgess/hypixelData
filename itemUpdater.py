import time
import mysql.connector
import os
from db import insertMany, select
from api import getItems, getItemFromCofl
        
def subtractRarity(rarity): 
    subtractedRarity = 'UNKNOWN'
    
    #GET SKYCOLF RARITY AND SET SUBTRACTED TO ONE BELOW
    if (rarity == 'COMMON'):
        subtractedRarity = 'COMMON'
    elif (rarity == 'UNCOMMON'):
        subtractedRarity = 'COMMON'
    elif (rarity == 'RARE'):
        subtractedRarity = 'UNCOMMON'
    elif (rarity == 'EPIC'):
        subtractedRarity = 'RARE'
    elif (rarity == 'LEGENDARY'):
        subtractedRarity = 'EPIC'
    elif (rarity == 'SPECIAL'):
        subtractedRarity = 'LEGENDARY'
    elif (rarity == 'VERY_SPECIAL'):
        subtractedRarity = 'SPECIAL'
    elif (rarity == 'MYTHIC'):
        subtractedRarity = 'VERY_SPECIAL'
    elif (rarity == 'SUPREME'):
        subtractedRarity = 'MYTHIC'
    elif (rarity == 'DIVINE'):
        subtractedRarity = 'SUPREME'
    
    return subtractedRarity;

def getItemsValues():
    itemsFromApi = getItems()
    itemsFromDB = select('SELECT id, idHypixel FROM item')

    if not itemsFromDB:
        print('⚠️ SELECT from item returned nothing')
        return
    
    if not itemsFromApi:
        print('⚠️ getItems returned nothing')
        return

    items = []
    
    # Addings PETS to items
    for itemFromDB in itemsFromDB:
        if (str(itemFromDB[1]).startswith('PET_')):
            itemInfo = getItemFromCofl(itemFromDB[1])
            
            if not itemInfo:
                print('⚠️ getItemFromCofl returned nothing, trying again in 3sec...')
                time.sleep(3)
                itemInfo = getItemFromCofl(itemFromDB[1])
                if not itemInfo:
                    print('⚠️ getItemFromCofl returned nothing again, skipping...')
                    continue
                

            id = itemFromDB[0]
            idHypixel = itemFromDB[1]
            name = itemInfo['name']
            rarity = itemInfo['tier']
            category = itemInfo['category']
            iconURL = itemInfo['iconUrl']
            npcSellPrice = int(itemInfo['npcSellPrice'])
            updatedOn = str(int(time.time()))

            item = (id, idHypixel, name, rarity, category, iconURL, npcSellPrice, updatedOn)
            print('✅ Adding item to list: ' + item[2])
            items.append(item)
    
    for itemFromDB in itemsFromDB:
        for itemFromApi in itemsFromApi:
            
            idDB = itemFromDB[1]
            itemId = idDB

            if (str(idDB).startswith('PET_')):
                continue
            
            if '?' in idDB:
                param = '?'
                itemId = idDB.split('?')[0]
                param += idDB.split('?')[1]
            
            if(itemId == itemFromApi['id']):
                itemInfo = getItemFromCofl(idDB)
                
                if not itemInfo:
                    print('⚠️ getItemFromCofl returned nothing, trying again in 3sec...')
                    time.sleep(3)
                    itemInfo = getItemFromCofl(idDB)
                    if not itemInfo:
                        print('⚠️ getItemFromCofl returned nothing again, skipping...')
                        continue
                    

                id = itemFromDB[0]
                idHypixel = itemFromDB[1]
                name = itemInfo['name']
                iconURL = itemInfo['iconUrl']

                if ('tier' in itemFromApi):
                    rarity = itemFromApi['tier']
                else:
                    rarity = subtractRarity(itemInfo['tier'])

                if ('category' in itemFromApi):
                    category = itemFromApi['category']
                else:
                    category = itemInfo['category']
                
                if ('npcSellPrice' in itemFromApi):
                    npcSellPrice = int(itemFromApi['npcSellPrice'])
                else:
                    npcSellPrice = int(itemInfo['npcSellPrice'])
                
                updatedOn = str(int(time.time()))
                
                item = (id, idHypixel, name, rarity, category, iconURL, npcSellPrice, updatedOn)
                print('✅ Adding item to list: ' + item[2])
                items.append(item)
    
    print(f'✅ Items list finished ({str(len(items))} items)')
    return items

def updateItemTable():
    values = getItemsValues()

    if not values:
        print('⚠️ getItemsValues returned nothing')
        return
    
    insertQuery = """
                        INSERT INTO item (id, idHypixel, name, rarity, category, iconURL, npcSellPrice, updatedOn) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE
                        id = VALUES(id),
                        idHypixel = VALUES(idHypixel),
                        name = VALUES(name),
                        rarity = VALUES(rarity),
                        category = VALUES(category),
                        iconURL = VALUES(iconURL),
                        npcSellPrice = VALUES(npcSellPrice),
                        updatedOn = VALUES(updatedOn)
                    """       
    print('✅ Inserting/updating table item...')
    insertMany(insertQuery, values)