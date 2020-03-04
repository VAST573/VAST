# A cve class that is used to make cve objects to store relevant information
#
# @author Isaiah Doyle
# @version 2020.02.19

class Cve:
    # init method that constructs a instance of a cve
    def __init__(self, cveIdNumber, impactScoreV2, impactScoreV3, lastPublishedDate, lastModifiedDate, description, keywordID):
        self.cveIdNumber = cveIdNumber
        self.impactScoreV2 = impactScoreV2
        self.impactScoreV3 = impactScoreV3
        self.lastPublishedDate = lastPublishedDate
        self.lastModifiedDate = lastModifiedDate
        self.description = description
        self.keywordID = keywordID

    # Returns the cveIdNumber for the cve as a string.
    def getcveIdNumber(self):
        return self.cveIdNumber

    # Returns the impactScore of the cve as a string.
    def getimpactScoreV2(self):
        return self.impactScoreV2

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

    def getkeywordID(self):
        return self.keywordID

