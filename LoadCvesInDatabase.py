import pymysql
import mysql.connector
from mysql.connector import errorcode
import CveClass

def addCvesToDatabase(cveInstanceList):
    try:
        cnx = mysql.connector.connect(user='cyberuser', password='cyber',
                              host='127.0.0.1',
                              database='VAST')
        cursor = cnx.cursor(buffered=True)
        cursor.execute("USE VAST") # select the database
        #cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)
        for cve in cveInstanceList:
            insertCVE = ("INSERT INTO CVE_Alerts " 
                        "(CVE_Number, description, impactV2, impactV3, publish_date, modified_date)"
                        "VALUES  (%s, %s, %s, %s, %s, %s)")
            cveInfo = (cve.getcveIDNumber(), cve.getDescription(), cve.getimpactScoreV2(), cve.getimpactScoreV3(), cve.getlastPublishedDate(),cve.getLastModifiedDate())
            cursor.execute(insertCVE,cveInfo)
        print('cves where addded to the database')
        cnx.commit()

    except mysql.connector.Error as error:
        print("Failed to insert record into CVE table {}".format(error))
        print(type(error))

    finally:
        cnx.close()





