from time import sleep
import mysql.connector
import os
from api import getItems, getItemFromCofl

def getItemsFromDB():
    try:        
        connection = mysql.connector.connect(host=os.environ.get('MYSQL_HOST'),
                                            database=os.environ.get('MYSQL_DATABASE'),
                                            user=os.environ.get('MYSQL_USER'),
                                            password=os.environ.get('MYSQL_PASSWORD'))

        if connection.is_connected():
            print("CONNECTED IN getItemsFromDB")
            cursor = connection.cursor()

            cursor.execute("SELECT id, itemId FROM iteminfo")

            items = cursor.fetchall()
            
    except mysql.connector.Error as e:
        print('SELECT ERROR IN ITEMS INFO')
        print("Error while connecting to MySQL", e)
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
            return items

def getItemsInfoValues():
    itemsFromApi = getItems()
    itemsFromDB = getItemsFromDB()

    if not itemsFromDB:
        print('No items in DB')
        return
    else:
        print('Items in DB returned')

    if not itemsFromApi:
        print('No items in API')
        return
    else:
        print('Items in API returned')

    items = []

    for itemFromDB in itemsFromDB:
        for itemFromApi in itemsFromApi:
            if (str(itemFromDB[1]).startswith('PET_')):
                itemInfo = getItemFromCofl(itemFromDB[1])

                id = itemFromDB[0]
                itemId = itemFromDB[1]
                name = itemInfo['name']
                rarity = itemInfo['tier']
                category = itemInfo['category']
                iconUrl = itemInfo['iconUrl']
                npcSellPrice = int(itemInfo['npcSellPrice'])

                items.append((id, itemId, npcSellPrice, name, rarity, category, iconUrl))

            if(itemFromDB[1] == itemFromApi['id']):
                itemInfo = getItemFromCofl(itemFromDB[1])
                
                if not itemInfo:
                    print('ItemInfo returned nothing, trying again in 3sec...')
                    sleep(3)
                    itemInfo = getItemFromCofl(itemFromDB[1])
                    if not itemInfo:
                        print('ItemInfo returned nothing again, skipping...')
                        continue
                else:
                    print('Adding to list: ', itemInfo['name'])

                id = itemFromDB[0]
                itemId = itemFromDB[1]
                name = itemFromApi['name']
                iconUrl = itemInfo['iconUrl']

                if ('tier' in itemFromApi):
                    rarity = itemFromApi['tier']
                else:
                    rarity = 'UNKNOWN'

                if ('category' in itemFromApi):
                    category = itemFromApi['category']
                else:
                    category = 'UNKNOWN'
                
                if ('npcSellPrice' in itemFromApi):
                    npcSellPrice = int(itemFromApi['npcSellPrice'])
                else:
                    npcSellPrice = 0
                
                items.append((id, itemId, npcSellPrice, name, rarity, category, iconUrl))
    
    print('Items list finished')
    return items

def updateItemsInfo():
    values = getItemsInfoValues()

    if not values:
        print('No items to update')
        return

    try:        
        connection = mysql.connector.connect(host=os.environ.get('MYSQL_HOST'),
                                            database=os.environ.get('MYSQL_DATABASE'),
                                            user=os.environ.get('MYSQL_USER'),
                                            password=os.environ.get('MYSQL_PASSWORD'))
        
        if connection.is_connected():
            print("CONNECTED IN updateItemsInfo")
            cursor = connection.cursor()
            insertQuery = """
                            INSERT INTO iteminfo (id, itemId, npcSellPrice, name, rarity, category, iconUrl) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s) 
                            ON DUPLICATE KEY UPDATE
                            id = VALUES(id),
                            itemId = VALUES(itemId),
                            npcSellPrice = VALUES(npcSellPrice),
                            name = VALUES(name),
                            rarity = VALUES(rarity),
                            category = VALUES(category),
                            iconUrl = VALUES(iconUrl)
                        """
            
            cursor.executemany(insertQuery, values)
            connection.commit()
            print("Records inserted/updated successfully into ITEMINFO table")
            
    except mysql.connector.Error as e:
        print('INSERT ERROR IN ITEMINFO')
        print("Error while connecting to MySQL", e)
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")