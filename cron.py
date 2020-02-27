import os
# This cron file runs every 2 hours.

os.system('wget -O /home/ubuntu/SWEProject/nvdFileLocation/recent.zip https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.zip ')
os.system('unzip -o /home/ubuntu/SWEProject/nvdFileLocation/recent.zip -d /home/ubuntu/SWEProject/nvdFileLocation')

