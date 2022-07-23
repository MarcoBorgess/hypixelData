from api import getBins
from db import select, insertMany

def getAhItemsValues():
    
    ids = select('SELECT idHypixel FROM ah')

    values = getBins(ids)
    return values

def updateAh():
    values = getAhItemsValues()

    if not values:
        print('⚠️ Nothing returned in getAhItemsValues, skipping auctions update.')
        return
    
    insertQuery = """
                    INSERT INTO ah (idHypixel, bin, secondBin, updatedOn) 
                    VALUES (%s, %s, %s, %s) 
                    ON DUPLICATE KEY UPDATE
                    idHypixel = VALUES(idHypixel),
                    bin = VALUES(bin),
                    secondBin = VALUES(secondBin),
                    updatedOn = VALUES(updatedOn)
                """
    
    print('✅ Inserting/updating table ah...')
    insertMany(insertQuery, values)
    