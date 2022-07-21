import mysql.connector
import os
from api import getBins

def getBinsSelect():
    try:        
        connection = mysql.connector.connect(host=os.environ.get('MYSQL_HOST'),
                                            database=os.environ.get('MYSQL_DATABASE'),
                                            user=os.environ.get('MYSQL_USER'),
                                            password=os.environ.get('MYSQL_PASSWORD'))

        if connection.is_connected():
            print("CONNECTED IN getBinsSelect")
            cursor = connection.cursor()

            cursor.execute("SELECT id, itemId, params FROM bins")

            ids = cursor.fetchall()
            
            
    except mysql.connector.Error as e:
        print('SELECT ERROR')
        print("Error while connecting to MySQL", e)
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

        values = getBins(ids)
        return values

def updateBins():
    values = getBinsSelect()

    if not values:
        print('No bins to update')
        return

    try:        
        connection = mysql.connector.connect(host=os.environ.get('MYSQL_HOST'),
                                            database=os.environ.get('MYSQL_DATABASE'),
                                            user=os.environ.get('MYSQL_USER'),
                                            password=os.environ.get('MYSQL_PASSWORD'))
        
        if connection.is_connected():
            print("CONNECTED IN updateBins")
            cursor = connection.cursor()
            insertQuery = """
                            INSERT INTO bins (id, itemId, bin, secondBin, updatedOn) 
                            VALUES (%s, %s, %s, %s, %s) 
                            ON DUPLICATE KEY UPDATE
                            id = VALUES(id),
                            itemId = VALUES(itemId),
                            bin = VALUES(bin),
                            secondBin = VALUES(secondBin),
                            updatedOn = VALUES(updatedOn)
                        """
                                   
            cursor.executemany(insertQuery, values)
            connection.commit()
            print("Records inserted/updated successfully into BINS table")
            
    except mysql.connector.Error as e:
        print('INSERT ERROR IN BINS')
        print("Error while connecting to MySQL", e)
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")