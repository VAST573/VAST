#!/usr/bin/env python3

# A current activity class that makes a current activity post to store information from
# the National Cyber Awareness System website.
#
# @Author Isaiah Doyle
# @version 2020.02.21


class NcasCAObject:
    # init method that constructs a Current activity instance post from the ncas website
    def __init__(self, entryTitle, entryDate, entryDescription, entryLink, keywordID):
        self.entryTitle = entryTitle
        self.entryDate = entryDate
        self.entryDescription = entryDescription
        self.entryLink = entryLink
        self.keywordID = keywordID


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


    # Returns the keyword ID as a int
    def getKeywordID(self):
        return self.keywordID


    # Used to determine if ncasCAObject is the same or not
    def __eq__(self, other):
        return self.entryTitle.lower() == other.entryTitle.lower()\
                and self.entryDescription.lower() == other.entryDescription.lower()
                #and self.entryDate.date() == other.entryDate.date()


    # The hash for a ncasCAObject 
    def __hash__(self):
        return hash((self.entryTitle, self.entryDescription))

