#!/usr/bin/env python3  
import os
import CveClass
import ParseJsonFile
import ncasAlertClass
import ncasAlertScraper
import ncasCurrentActivityScraper
import LoadAlertsIntoDatabase
import logging
import time
import grabUsersFromDatabase
# This main file runs every 2 hours and 30 minutes by crontab.
#
# @Author Isaiah Doyle
# @Version 2020.04.03

start = time.time()
# goes the nvd data feed website, downloads and overwrites the nvd recent json file
os.system('wget -O /home/ubuntu/SWEProject/nvdFileLocation/recent.zip https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.zip ')
os.system('unzip -o /home/ubuntu/SWEProject/nvdFileLocation/recent.zip -d /home/ubuntu/SWEProject/nvdFileLocation')

# the file we want to read and traverse
recent_nvd_file = '/home/ubuntu/SWEProject/nvdFileLocation/nvdcve-1.1-recent.json'

# The nvd json file as a dict
nvd_json_dict = ParseJsonFile.openFile(recent_nvd_file)

# traverse the nvd dict to get all the cve information as a list of cve's
cveInstanceList = ParseJsonFile.getCveInformation(nvd_json_dict)

# the alert from the ncas Alert Scrapper module we want to add to the database 
ncasAlert = ncasAlertScraper.ncasAlert

# the list of current activity post we want to add to the database
ncasCurrentActivityPostList = ncasCurrentActivityScraper.newPostList

# this method takes in all the alerts and adds them to the database
LoadAlertsIntoDatabase.addToDatabase(cveInstanceList, ncasAlert, ncasCurrentActivityPostList)

#this method is the main function call to send emails to all the users in teh database
grabUsersFromDatabase.grabFromDatabase()

#Logs the time thr program was run and how long it took
logging.basicConfig(level=logging.DEBUG, filename="LOGFILE", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info("\nfile was run by crontab at this time." +  'It took ' + str(time.time()-start) + "seconds for program to run")

logging.info(cveInstanceList)
