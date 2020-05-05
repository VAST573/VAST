#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import ncasCurrentActivityClass
import datetime
import pickle
import ParseJsonFile

# This module web scrapes the ncas current activity page to find and grab
# all the current activity posts on the website.
# A post has a title, description, date, and a read more link for more detail about the post.
#
# @Author Isaiah Doyle
# @Version 2020.02.24


usCertGov = 'https://www.us-cert.gov'  # used to create a full link
url = 'https://www.us-cert.gov/ncas/current-activity'  # the url of the website we want to scrape
listofEntrys = []  # stores the list of all the entry's
setofEntrys = set([]) 
current_date = datetime.date.today()

# Makes a request to a web page and requests the data from the page.
# The content from data needs to be parsed in html format.
# Then call the getCurrentEntrys method and pass it the content to get the entrys
def getncasCurrentActivity(url):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    getCurrentEntrys(content)


# This method goes through the content on the website, loops through each post,
# gets the information about the post, then makes a entry instance
# and appends the entry to the listofEntrys list
def getCurrentEntrys(content):
    for post in content.findAll('div', attrs={"class": "views-row"}):
        entryTitle = getEntryTitle(post)
        entryDate = getEntryDate(post)
        entryDescription = getEntryDescription(post)
        entryLink = getEntryLink(post)
        entryKeywordID = ParseJsonFile.CheckForKeywords(entryTitle)
        entry = ncasCurrentActivityClass.NcasCAObject(entryTitle, entryDate, entryDescription, entryLink, entryKeywordID)
        if entryKeywordID > 0:
            if entry.getEntryDate().date() == current_date:
                listofEntrys.append(entry)



# helper function that finds the title of the entry using the html tag
# returns the title as a string
def getEntryTitle(post):
    entryTitle = post.find('h3', attrs={"class": "entry-title"})
    soup = BeautifulSoup(str(entryTitle),'lxml')
    entryTitle = soup.get_text()
    return entryTitle


# helper function that finds the date the entry was published
# returns the entry date as a string
def getEntryDate(post):
    entryDate = post.find('div', attrs={"class": "entry-date"}).text.encode('utf-8')  # finds entry date ( as a string )
    stringDate = str(entryDate)
    stringDateList = stringDate.split(',')
    stringDate = stringDateList[1] + stringDateList[2]
    stringDate = stringDate[1 : (len(stringDate) - 1)]
    entryDate = datetime.datetime.strptime(stringDate, '%B %d %Y')
    cur = datetime.datetime.now()
    newEntryDate = datetime.datetime(entryDate.year, entryDate.month, entryDate.day, cur.hour, cur.minute, cur.second)
    return newEntryDate


# helper function that finds the description of the entry
# returns the description as a string
def getEntryDescription(post):
    entryDescription = post.find('div', attrs={"class": "views-field views-field-body"})
    soup = BeautifulSoup(str(entryDescription), 'lxml')
    entryDescription = soup.get_text()
    return entryDescription


# helper function that finds the read more link fo the entry
# returns the link as a string
def getEntryLink(post):
    linkField = post.find('div', attrs={"class": "views-field views-field-view-node read-more"})
    linkFieldContent = linkField.find('span', attrs={"class": "field-content"})
    LinkWithHtlmTags = linkFieldContent.find('a')
    link = LinkWithHtlmTags.get('href')
    return usCertGov + link


# Function that uses Serialization to determine if a post is new
# if a post is new, add it to the returned list and add it to
# the serialized set. 
def checkCurrentPostsWithPreviousPosts():
    #newPosts = []
    #with open('ncasCurrentActivitySerialization','rb') as entrySet_saved_to_file:
       # previousEntrySet = pickle.load(entrySet_saved_to_file)
        #for post in listofEntrys:
           # if post not in previousEntrySet:
               # newPosts.append(post)
               # previousEntrySet.add(post)
        #entrySet_saved_to_file.close()
    #with open('ncasCurrentActivitySerialization','wb') as entrySet_saved_to_file:
               # pickle.dump(previousEntrySet,entrySet_saved_to_file)
               # entrySet_saved_to_file.close()
    return listofEntrys


""" calling functions  """
getncasCurrentActivity(url)
newPostList = checkCurrentPostsWithPreviousPosts()


