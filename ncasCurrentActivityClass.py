# A current activity class that makes a current activity post to store information from
# the National Cyber Awareness System website.
#
# @Author Isaiah Doyle
# @version 2020.02.21


class NcasCAObject:
    # init method that constructs a Current activity instance post from the ncas website
    def __init__(self, entryTitle, entryDate, entryDescription, entryLink):
        self.entryTitle = entryTitle
        self.entryDate = entryDate
        self.entryDescription = entryDescription
        self.entryLink = entryLink

    # Returns the entry title as a string.
    def getEntryTitle(self):
        return self.entryTitle

    # Returns the entry date as a string.
    def getEntryDate(self):
        return self.entryDate

    # Returns the entry description as a string
    def getEntryDescription(self):
        return self.entryDescription

    # Returns the entry Link as a string
    def getEntryLink(self):
        return self.entryLink

