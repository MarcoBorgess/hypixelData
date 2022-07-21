import mysql.connector
import os
from api import getBazaar

def updateBazaar():
    try:
        values = getBazaar()
        
        if not values:
            print('No bazaar to update')
            return
        
        connection = mysql.connector.connect(host=os.environ.get('MYSQL_HOST'),
                                            database=os.environ.get('MYSQL_DATABASE'),
                                            user=os.environ.get('MYSQL_USER'),
                                            password=os.environ.get('MYSQL_PASSWORD'))

        if connection.is_connected():
            cursor = connection.cursor()
            
            insertQuery = """
                            INSERT INTO bazaar (itemId, sellPrice, buyPrice, sellVolume, buyVolume, sellMovingWeek, buyMovingWeek, sellOrders, buyOrders, updatedOn) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                            ON DUPLICATE KEY UPDATE
                            itemId = VALUES(itemId),
                            sellPrice = VALUES(sellPrice),
                            buyPrice = VALUES(buyPrice),
                            sellVolume = VALUES(sellVolume),
                            buyVolume = VALUES(buyVolume),
                            sellMovingWeek = VALUES(sellMovingWeek),
                            buyMovingWeek = VALUES(buyMovingWeek),
                            sellOrders = VALUES(sellOrders),
                            buyOrders = VALUES(buyOrders),
                            updatedOn = VALUES(updatedOn);
                            
                            INSERT INTO itemInfo (itemId)
                            VALUES (%s)
                            ON DUPLICATE KEY UPDATE
                            itemId = VALUES(itemId);
                        """
            
            cursor.executemany(insertQuery, values)
            connection.commit()
            print("Records inserted/updated successfully into BAZAAR table")
            
    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        