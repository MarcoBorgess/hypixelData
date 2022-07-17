import mysql.connector
import os
from api import getBazaar

def updateBazaar():
    try:
        connection = mysql.connector.connect(host=os.environ.get('MYSQL_HOST'),
                                            database=os.environ.get('MYSQL_DATABASE'),
                                            user=os.environ.get('MYSQL_USER'),
                                            password=os.environ.get('MYSQL_PASSWORD'))
        if connection.is_connected():
            cursor = connection.cursor()
            
            insertQuery = """
                            INSERT INTO bazaar (id, sellPrice, buyPrice, sellVolume, buyVolume, sellMovingWeek, buyMovingWeek, sellOrders, buyOrders, updatedOn) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                            ON DUPLICATE KEY UPDATE
                            id = VALUES(id),
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
            values = getBazaar()
            
            cursor.executemany(insertQuery, values)
            connection.commit()
            print("Records inserted/updated successfully into bazaar table")
            
    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        