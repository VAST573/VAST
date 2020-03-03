from bs4 import BeautifulSoup
import requests
import ncasAlertClass

# This module scraps the ncas alert website for the list of alerts.( the alerts are posted as links )
# then web scraps the most recent alert website and make a ncas alert instance that holds the
# information about that alert.
#
# @Author Isaiah Doyle
# @version


url = 'https://www.us-cert.gov/ncas/alerts'  # the url we want to scrape
listOfLinks = []  # list to store all of the alert links from the website
usCertGov = 'https://www.us-cert.gov'  # used to make a url


# Makes a request to a web page and requests the data from the page.
# The content from data needs to be parsed in html format.
# Passes the content to teh getAlertLinks method
def getAllOfAlerts(url):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    getAlertLinks(content)


# For each alert in the content, get the link and append it
# to the listOfLinks list
def getAlertLinks(content):
    for alert in content.findAll('span', attrs={'class': 'field-content'}):
        linkWithHtmlTags = alert.find('a')  # find the link including the html tags
        partOfLink = linkWithHtmlTags.get('href')  # get the link without the html tags ( as a string )
        FullLink = usCertGov + partOfLink  # makes a link we can go to
        listOfLinks.append(FullLink)  # put the link in the list of links list


# now scrape the most recent alert website
# returns a ncasAlert instance
def getRecentAlertInfo(url):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    # go to all the regions in content on the website that holds all the information
    for region in content.findAll('div', attrs={'class': 'region region-content'}):
        header = getAlertHeader(region)
        pageTitle = getAlertPageTitle(header)
        subTitle = getAlertSubTitle(header)
        releaseDate = getAlertReleaseDate(header)
        summaryList = getSummary(content)

        ncasAlert = ncasAlertClass.NcasAlert(pageTitle, subTitle, releaseDate, summaryList)
    return ncasAlert


# Helper function, finds the header of the section of the region
# returns the header of the region
def getAlertHeader(region):
    header = region.find('div', attrs={'id': 'ncas-header'})
    return header


# Helper function, finds the page title ( Ex. Alert AA20-049A )
# returns the pageTitle of the alert as a string
def getAlertPageTitle(header):
    pageTitle = header.find('h1', attrs={'id': 'page-title'})
    return pageTitle


# Helper function, finds the sub title ( what the alert is called Ex. Ransomware Impacting Pipeline Operations
# returns the subTitle of the alert as a string
def getAlertSubTitle(header):
    subTitle = header.find('h2', attrs={
        'id': 'page-sub-title'})
    return subTitle


# Helper function, finds the release date of the alert
# returns the release date of the alert as a string ( Ex. feb 20, 2020 )
def getAlertReleaseDate(header):
    releaseDate = header.find('div', attrs={
        'class': 'submitted meta-text'})
    return releaseDate


# Helper function, finds the  section that holds the summary of the alert
# then finds the field for the summary text
# returns the summary of the alert as a list
def getSummary(content):
    article = content.find('article', attrs={'role': 'article'})
    summaryField = article.find('div', attrs={
        'class': 'field field--name-body field--type-text-with-summary field--label-hidden field--item'})
    summaryList = []  # used to store each paragraph
    for info in summaryField.findAll('p'):  # loop that gets a paragraoh and stores it in the summaryList
        summaryList.append(info)
    return summaryList


""" calling functions to test """

#getAllOfAlerts(url)

#ncasAlert = getRecentAlertInfo(listOfLinks[0])

#print(ncasAlert.getSummaryList())
