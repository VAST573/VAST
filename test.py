#!/usr/bin/env python3

import json
import pandas as pd
import CveClass
import datetime
from datetime import timedelta
import logging


# This module takes in the nvd recent file.
# Parses the file for the information we want and makes
# cve objects for each cve in the file and stores them in a list
#
# @Author Isaiah Doyle
# @Version 2020.02.19

current_time_when_program_runs = datetime.datetime.now()

current_Time_minus_2_hours = current_time_when_program_runs - timedelta(hours = 2)

listofKeywords = ['Apple','Google','kill-port-process','Microsoft','IDM','IBM','Cisco','Debian','Redhat','Oracle','Adobe','WordPress','Drupal','FluxBB','UseBB','Canonical','Amazon','Linux','Mozilla','Wireshark','SUSE','Apache','Mcafee','PHP','Windows','Firefox','iPadOS','Netgear','iOS','macOS']


# opens the provided json file and reads the file
def openFile(file):
    with open(file, 'r') as my_file:
        nvd_file = my_file.read()
    return json.loads(nvd_file)


# Loops through the cve items and returns a list of cves.
def getCveInformation(nvd_json_dict):
    cveList = []
    index = 0
    df = pd.DataFrame(nvd_json_dict)
    num_of_cves = len(df.index) - 1
    while index <= num_of_cves:
        cve_data = df.iloc[index]
        cve_items = cve_data['CVE_Items']
        cve_info = cve_items['cve']
        cve_id_number = FindCveIdNumber(cve_info)
        cve_last_published_date = FindLastPublishedDate(cve_items)
        cve_last_modified_date = FindLastModifiedDate(cve_items)
        cve_impact_scoreV2 = FindCveImpactScoreV2(cve_items)
        cve_impact_scoreV3 = FindCveImpactScoreV3(cve_items)
        cve_description = FindDescription(cve_info)
        cve_keyWordID = CheckForKeywords(cve_description)
        if cve_keyWordID > 0:
            if current_time_when_program_runs.date() == cve_last_published_date.date():
                cve_object = CveClass.Cve(cve_id_number, cve_impact_scoreV2, cve_impact_scoreV3,
                        cve_last_published_date, cve_last_modified_date, cve_description, cve_keyWordID)
                cveList.append(cve_object)
                print(index, cve_impact_scoreV2, cve_impact_scoreV3)
        index+=1
    return cveList

# helper function to traverse the cve info dict and returns the cve ID Number
# Ex. CVE_2020-1984
# cve_ID_Number holds the cve ID number as a string
def FindCveIdNumber(cve_info):
    cve_data_meta = cve_info['CVE_data_meta']
    cve_id_number = cve_data_meta['ID']
    return cve_id_number


# helper function to traverse the cve and returns the Last Modified Date for the cve
def FindLastModifiedDate(cve_items):
    cve_last_modified_date = cve_items['lastModifiedDate']
    firstSplit = cve_last_modified_date.split('T')
    SecondSplit = firstSplit[1].split('Z')
    date_str = firstSplit[0]
    time_str = SecondSplit[0]
    dateTime_str = date_str +' '+ time_str
    dateTime_object = datetime.datetime.strptime(dateTime_str, '%Y-%m-%d %H:%M')
    dateTime_To_Est = dateTime_object - timedelta(hours = 5)
    return dateTime_To_Est

# helper fuction to traverse the cve and returns the last Published Date 
def FindLastPublishedDate(cve_items):
    cve_last_published_date = cve_items['publishedDate']
    firstSplit = cve_last_published_date.split('T')
    SecondSplit = firstSplit[1].split('Z')
    date_str = firstSplit[0]
    time_str = SecondSplit[0]
    dateTime_str = date_str +' '+ time_str
    dateTime_object = datetime.datetime.strptime(dateTime_str, '%Y-%m-%d %H:%M')
    dateTime_To_Est = dateTime_object - timedelta(hours = 5)
    return dateTime_To_Est


# helper function to traverse the cve info dict and returns the description
def FindDescription(cve_info):
    description = cve_info['description']
    description_data = description['description_data'][0]
    value = description_data['value']
    return value


# helper function to traverse the cve dict and returns the description
def FindCveImpactScoreV2(cve_items):
    cve_impact_score = 0.0
    cve_impact = cve_items['impact']
    v2Keys = cve_impact.keys()
    if 'baseMetricV2' in v2Keys:
        cve_impact_metric_version = cve_impact['baseMetricV2']
        cve_impact_score = cve_impact_metric_version['impactScore']
    return cve_impact_score


# helper function to return impact score V3
def FindCveImpactScoreV3(cve_items):
    cve_impact_score = 0.0
    cve_impact = cve_items['impact']
    v3Keys = cve_impact.keys()
    if 'baseMetricV3' in v3Keys:
        cve_impact_metric_version = cve_impact['baseMetricV3']
        cve_impact_score = cve_impact_metric_version['impactScore']
    return cve_impact_score


# helper fucniton to check if decsription of  cve has one of our keywords
def CheckForKeywords(description):
    for keyword in listofKeywords:
        if keyword.lower() in description.lower():
            return listofKeywords.index(keyword) + 1
            break
    return 0


# checsk if cve was published in the last two hours  
def PublishedLastTwoHours(cve_last_published_date):
    if (cve_last_published_date >= current_Time_minus_2_hours):
        return True
    return False 

recent_nvd_file = '/home/ubuntu/SWEProject/nvdFileLocation/nvdcve-1.1-recent.json'

# The nvd json file as a dict
nvd_json_dict = openFile(recent_nvd_file)

# traverse the nvd dict to get all the cve information as a list of cve's
cveInstanceList = getCveInformation(nvd_json_dict)

