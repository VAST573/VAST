import json
import CveClass

# This module takes in the nvd recent file.
# Parses the file for the information we want and makes
# cve objects for each cve in the file and stores them in a list
#
# @Author Isaiah Doyle
# @Version 2020.02.19


# opens the provided json file and reads the file
def openFile(file):
    with open(file, 'r') as my_file:
        nvd_file = my_file.read()
    return json.loads(nvd_file)


# Loops through the cve items and returns a list of cves.
def getCveInformation(nvd_json_dict):
    cve_items = nvd_json_dict['CVE_Items']
    cveList = []
    for cve in cve_items:
        cve_info = cve['cve']
        cve_id_number = FindCveIdNumber(cve_info)
        cve_last_published_date = FindLastPublishedDate(cve)
        cve_impact_score = FindCveImpactScore(cve)
        cve_description = FindDescription(cve_info)
        cve_object = CveClass.Cve(cve_id_number, cve_impact_score, cve_last_published_date, cve_description)
        cveList.append(cve_object)
    return cveList

# helper function to traverse the cve info dict and returns the cve ID Number
# Ex. CVE_2020-1984
# cve_ID_Number holds the cve ID number as a string
def FindCveIdNumber(cve_info):
    cve_data_meta = cve_info['CVE_data_meta']
    cve_id_number = cve_data_meta['ID']
    return cve_id_number


# helper function to traverse the cve and returns the Last Published date for the cve
def FindLastPublishedDate(cve):
    cve_last_published_date = cve['lastModifiedDate']
    return cve_last_published_date


# helper function to traverse the cve info dict and returns the description
def FindDescription(cve_info):
    cve_description = cve_info['description']
    cve_description_data = cve_description['description_data']
    description_breakdown = cve_description_data[0]
    description_value = description_breakdown['value']
    return description_value


# helper function to traverse the cve dict and returns the description
def FindCveImpactScore(cve):
    cve_impact = cve['impact']
    if 'baseMetricV2' in cve_impact.keys():
        cve_impact_metric_version = cve_impact['baseMetricV2']
        cve_impact_score = cve_impact_metric_version['impactScore']
    elif 'baseMetricV3' in cve_impact.keys():
        cve_impact_metric_version = cve_impact['baseMetricV3']
        cve_impact_score = cve_impact_metric_version['impactScore']
    else:
        cve_impact_score = 'No impact score available'
    return cve_impact_score


# the file we want to read and traverse
recent_nvd_file = '/home/ubuntu/SWEProject/nvdFileLocation/nvdcve-1.1-recent.json'


# The nvd json file as a dict
nvd_json_dict = openFile(recent_nvd_file)

# traverse the nvd dict to get all the cve information as a list of cve's
cveInstanceList = getCveInformation(nvd_json_dict)

print(cveInstanceList[0].getDescription())

