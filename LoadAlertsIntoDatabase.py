#!/usr/bin/env python3
import pymysql
import mysql.connector
from mysql.connector import errorcode
import CveClass
import ncasAlertScraper
import logging

# This modules main purpose is to connenect to the database and run some querys
# The querys will insert a cve into the CVE_Alerts table, a currrent activity post
# In the Current_Activities table, and a apt alert into the APT_Alerts table. 
#
# @author Isaiah Doyle, Alex
# @version 2020.04.03


#this functions takes in two list and one alert object and adds them to the database 
def addToDatabase(cveInstanceList,ncasAlert,ncasCurrentActivityPostList):
    try:
        cnx = mysql.connector.connect(user='cyberuser', password='cyber',
                              host='127.0.0.1',
                              database='VAST')
        cursor = cnx.cursor(buffered=True)

        insertCVE = ("INSERT INTO CVE_Alerts "\
                "(Keyword_id, CVE_Number, Description, impactV2, impactV3, Published_Date, Modified_Date)"\
                "VALUES  (%s, %s, %s, %s, %s, %s, %s)")

        insertPost =("INSERT INTO Current_Activities "\
                "(Title, Published_Date, Description, Relevant_Link, Keyword_id)"\
                "VALUES (%s, %s, %s, %s, %s)")
        
        insertAlert = ("INSERT INTO APT_Alerts " \
                        "(keyword_id, alert_number, release_date, alert_title, description)" \
                        "VALUES (%s, %s, %s, %s, %s)")

        check_if_cve_exists = "select * from CVE_Alerts where CVE_Number = %s and Published_Date = %s"

        check_if_ca_exists = ("select * from Current_Activities where Title = %s and Relevant_Link = %s")

        check_if_apt_exists = ("select * from APT_Alerts where alert_number = %s and alert_title = %s")

        # Loops through the cve list and add them to the database
        for cve in cveInstanceList:
             cinfo = (cve.getcveIDNumber(),cve.getlastPublishedDate())
             cursor.execute(check_if_cve_exists,cinfo)
             List = cursor.fetchall()
             if len(List) == 0:
                 cveInfo = (cve.getkeywordID(), cve.getcveIDNumber(), cve.getDescription(),
                         cve.getimpactScoreV2(), cve.getimpactScoreV3(), cve.getlastPublishedDate(),
                         cve.getLastModifiedDate())
                 cursor.execute(insertCVE,cveInfo)

        
        # Loops through the current Activity List and adds them to the database
        for post in ncasCurrentActivityPostList:
            cainfo = (post.getEntryTitle(),post.getEntryLink())
            cursor.execute(check_if_ca_exists,cainfo)
            calist = cursor.fetchall()
            if len(calist) == 0:
                postInfo = (post.getEntryTitle(), post.getEntryDate(), post.getEntryDescription(),
                        post.getEntryLink(), post.getKeywordID())
                cursor.execute(insertPost,postInfo)
        

        #If the nceas alert is a new one and matches one of our keywords, add it to the database
            if ncasAlert.getKeywordID() > 0:
                apinfo = (ncasAlert.ncasAlert.getPageTitle(), ncasAlert.getSubTitle())
                cursor.execute(check_if_apt_exists,apinfo)
                aptlist = cursor.fetchall()
                if len(aptlist) == 0:
                    alertInfo(ncasAlert.getKeywordID(), ncasAlert.getPageTitle(), ncasAlert.getReleaseDate(),\
                        ncasAlert.getSubTitle(),  ncasAlert.getSummaryList())
                    cursor.execute(insertAlert,alertInfo)

        cnx.commit()
        cnx.close()
    except mysql.connector.Error as error:
        print(error)
        print(type(error))
        logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
        logging.info("error", type(error))





