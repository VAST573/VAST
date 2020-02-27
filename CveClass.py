# A cve class that is used to make cve objects to store relevant information
#
# @author Isaiah Doyle
# @version 2020.02.19

class Cve:
    # init method that constructs a instance of a cve
    def __init__(self, cveIdNumber, impactScore, lastPublishedDate, description):
        self.cveIdNumber = cveIdNumber
        self.impactScore = impactScore
        self.lastPublishedDate = lastPublishedDate
        self.description = description

    # Returns the cveIdNumber for the cve as a string.
    def getcveIdNumber(self):
        return self.cveIdNumber

    # Returns the impactScore of the cve as a string.
    def getimpactScore(self):
        return self.impactScore

    # Returns the lastPublishedDate of the cve as a string.
    def getlastPublishedDate(self):
        return self.lastPublishedDate

    # Returns the description of the cve as a string.
    def getDescription(self):
        return self.description

