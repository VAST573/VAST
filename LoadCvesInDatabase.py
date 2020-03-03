import pymysql
import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='cyberuser', password='cyber',
                              host='127.0.0.1',
                              database='VAST')
cursor = cnx.cursor()

cursor.execute("USE VAST") # select the database
cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)

for (table_name,) in cursor:
    print(table_name)

cnx.close()


