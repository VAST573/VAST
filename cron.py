import os
import CveClass
import ParseJsonFile
import ncasAlertClass
import ncasAlertScraper
import ncasCurrentActivityScraper
import LoadCvesInDatabase
# This cron file runs every 2 hours.

os.system('wget -O /home/ubuntu/SWEProject/nvdFileLocation/recent.zip https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.zip ')
os.system('unzip -o /home/ubuntu/SWEProject/nvdFileLocation/recent.zip -d /home/ubuntu/SWEProject/nvdFileLocation')

# the file we want to read and traverse
recent_nvd_file = '/home/ubuntu/SWEProject/nvdFileLocation/nvdcve-1.1-recent.json'

# The nvd json file as a dict
nvd_json_dict = ParseJsonFile.openFile(recent_nvd_file)

# traverse the nvd dict to get all the cve information as a list of cve's
cveInstanceList = ParseJsonFile.getCveInformation(nvd_json_dict)
print(cveInstanceList)


LoadCvesInDatabase.addCvesToDatabase(cveInstanceList)

