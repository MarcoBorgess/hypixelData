from db import insertMany
from api import getBazaar

def updateBz():
    values = getBazaar()
        
    if not values:
        print('⚠️ Nothing returned in getBazaar, skipping bazaar update.')
        return
    
    insertQuery = """
                    INSERT INTO bz (idHypixel, sellPrice, buyPrice, sellVolume, buyVolume, sellMovingWeek, buyMovingWeek, sellOrders, buyOrders, updatedOn) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    ON DUPLICATE KEY UPDATE
                    idHypixel = VALUES(idHypixel),
                    sellPrice = VALUES(sellPrice),
                    buyPrice = VALUES(buyPrice),
                    sellVolume = VALUES(sellVolume),
                    buyVolume = VALUES(buyVolume),
                    sellMovingWeek = VALUES(sellMovingWeek),
                    buyMovingWeek = VALUES(buyMovingWeek),
                    sellOrders = VALUES(sellOrders),
                    buyOrders = VALUES(buyOrders),
                    updatedOn = VALUES(updatedOn)
                """  
                
    print('✅ Inserting/updating table bz...')
    insertMany(insertQuery, values)