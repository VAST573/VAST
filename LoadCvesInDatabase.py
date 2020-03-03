import pymysql
import mysql.connector
from mysql.connector import errorcode
import CveClass
def addCvesToDatabase(cveInstanceList):
    try:
        cnx = mysql.connector.connect(user='cyberuser', password='cyber',
                              host='127.0.0.1',
                              database='VAST')
        cursor = cnx.cursor()
        cursor.execute("USE VAST") # select the database
        cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)
        if not cveInstanceList:
            print("cve List is empty, no new updates")
            cnx.close()
        else:
            for cve in cveInstanceList:
                insertCVE = """INSERT INTO CVE_Alerts (cve_alert_id, CVE_Number, description, impactV2, impactV3, publish_date, modified_date) VALUES  ({}, {}, {}, {}, {}, {}))""".format(cve.getcveIDNumber, cve.getDescription, cve.getimpactScoreV2, cve.getimpactScoreV3, cve.getlastPublishedDate, cve.getLastModifiedDate)
                cursor.execute(insertCVE)

        cnx.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))





