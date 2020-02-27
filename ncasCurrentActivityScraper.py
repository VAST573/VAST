from bs4 import BeautifulSoup
import requests
import ncasCurrentActivityClass

# This module web scrapes the ncas current activity page to find and grab
# all the current activity posts on the website.
# A post has a title, description, date, and a read more link for more detail about the post.
#
# @Author Isaiah Doyle
# @Version 2020.02.24


usCertGov = 'https://www.us-cert.gov'  # used to create a full link
url = 'https://www.us-cert.gov/ncas/current-activity'  # the url of the website we want to scrape
listofEntrys = []  # stores the list of all the entry's


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
        entry = ncasCurrentActivityClass.NcasCAObject(entryTitle, entryDate, entryDescription, entryLink)
        listofEntrys.append(entry)


# helper function that finds the title of the entry using the html tag
# returns the title as a string
def getEntryTitle(post):
    entryTitle = post.find('h3', attrs={"class": "entry-title"}).text.encode('utf-8')
    return entryTitle


# helper function that finds the date the entry was published
# returns the entry date as a string
def getEntryDate(post):
    entryDate = post.find('div', attrs={"class": "entry-date"}).text.encode('utf-8')  # finds entry date ( as a string )
    stringDate = str(entryDate)
    stringDateList = stringDate.split(',')
    entryDate = stringDateList[1] + stringDateList[2]
    return entryDate


# helper function that finds the description of the entry
# returns the description as a string
def getEntryDescription(post):
    entryDescription = post.find('div', attrs={"class": "views-field views-field-body"}).text.encode('utf-8')
    return entryDescription


# helper function that finds the read more link fo the entry
# returns the link as a string
def getEntryLink(post):
    linkField = post.find('div', attrs={"class": "views-field views-field-view-node read-more"})
    linkFieldContent = linkField.find('span', attrs={"class": "field-content"})
    LinkWithHtlmTags = linkFieldContent.find('a')
    link = LinkWithHtlmTags.get('href')
    return usCertGov + link


""" calling functions to test """

getncasCurrentActivity(url)
print(listofEntrys[0].getEntryDescription())

