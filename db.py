import mysql.connector
import os

def connect():
    print('✅ Connecting to DB...')        
    connection = mysql.connector.connect(host=os.environ.get('MYSQL_HOST'),
                                        database=os.environ.get('MYSQL_DATABASE'),
                                        user=os.environ.get('MYSQL_USER'),
                                        password=os.environ.get('MYSQL_PASSWORD'))
    
    return connection

def select(query):
    try:
        connection = connect()

        if connection.is_connected():
            print("✅ Connected to DB, executing query...")
            
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            
    except mysql.connector.Error as e:
        print("⚠️ Error while connecting to MySQL", e)
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("✅ MySQL connection is closed.")
            print("✅ Select complete, returning result...")
            return result
        
def insert(query):
    try:
        connection = connect()

        if connection.is_connected():
            print("✅ Connected to DB, executing query...")
            
            cursor = connection.cursor()
            try:
                cursor.execute(query)
                connection.commit()
                print("✅ Insert/update complete")
            except:
                connection.rollback()
                print("⚠️ Insert/update failed")
            
    except mysql.connector.Error as e:
        print("⚠️ Error while connecting to MySQL", e)
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("✅ MySQL connection is closed.")

def insertMany(query, values):
    try:
        connection = connect()

        if connection.is_connected():
            print("✅ Connected to DB, executing query...")
            
            cursor = connection.cursor()
            try:
                cursor.executemany(query, values)
                connection.commit()
                print("✅ Insert/update complete")
            except e:
                connection.rollback()
                print("⚠️ Insert/update failed" + e)
            
    except mysql.connector.Error as e:
        print("⚠️ Error while connecting to MySQL", e)
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("✅ MySQL connection is closed.")
            