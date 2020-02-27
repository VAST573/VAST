# this module is a national cyber awarness systen akert class.
# An alert has a page title, sub title, a release date and a summry List
#
# @Author Isaiah Doyle
# @Version 202.02.21


class NcasAlert:
    # init method that constructs a alert instance from the ncas alert website
    def __init__(self, pageTitle, subTitle, releaseDate, summaryList):
        self.pageTitle = pageTitle
        self.subTitle = subTitle
        self.releaseDate = releaseDate
        self.summaryList = summaryList

    # returns the page title as a string
    def getPageTitle(self):
        return self.pageTitle

    # returns the sub title as a string
    def getSubTitle(self):
        return self.subTitle

    # returns the release date as a string
    def getReleaseDate(self):
        return self.releaseDate

    # returns the summary list
    def getSummaryList(self):
        return self.summaryList

