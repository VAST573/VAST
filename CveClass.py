# #!/usr/bin/env python3
# A cve class that is used to make cve objects to store relevant information
#
# @author Isaiah Doyle, Alex
# @version 2020.02.19

class Cve:
    # init method that constructs a instance of a cve
    def __init__(self, cveIDNumber, impactScoreV2, impactScoreV3, lastPublishedDate, lastModifiedDate, description, keywordID):
        self.cveIDNumber = cveIDNumber
        self.impactScoreV2 = impactScoreV2
        self.impactScoreV3 = impactScoreV3
        self.lastPublishedDate = lastPublishedDate
        self.lastModifiedDate = lastModifiedDate
        self.description = description
        self.keywordID = keywordID

    #'tostring' for CVE Object    
    def __str__(self):
        return 'CVE Number: {} \nImpact Score: {}\nDesc: {}\n'.format(self.cveIDNumber, self.impactScoreV3, self.description)
    
    
    # how the CVE Object is printed/repr 
    def __repr__(self):
        return self.__str__()


    # Returns the cveIdNumber for the cve as a string.
    def getcveIDNumber(self):
        return self.cveIDNumber


    # Returns the impactScore Version 2 of the cve as a string.
    def getimpactScoreV2(self):
        return self.impactScoreV2


    # Returns the impactScore Version 3 of the cve as a string.
    def getimpactScoreV3(self):
        return self.impactScoreV3


    # Returns the lastPublishedDate of the cve as a dateTime Object.
    def getlastPublishedDate(self):
        return self.lastPublishedDate


    # Returns the last Modified date of the cve as a dateTime Object.
    def getLastModifiedDate(self):
        return self.lastModifiedDate


    # Returns the description of the cve as a string.
    def getDescription(self):
        return self.description


    # Retunrs the keyword ID 
    def getkeywordID(self):
        return self.keywordID

