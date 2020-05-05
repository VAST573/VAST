#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import ncasAlertClass
import datetime
import pickle
import ParseJsonFile

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
        keywordID = ParseJsonFile.CheckForKeywords(subTitle)
        ncasAlert = ncasAlertClass.NcasAlert(pageTitle, subTitle, releaseDate, summaryList,keywordID)
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
    soup = BeautifulSoup(str(pageTitle), 'lxml')
    pageTitle = soup.get_text()
    return pageTitle


# Helper function, finds the sub title ( what the alert is called Ex. Ransomware Impacting Pipeline Operations
# returns the subTitle of the alert as a string
def getAlertSubTitle(header):
    subTitle = header.find('h2', attrs={
        'id': 'page-sub-title'})
    soup = BeautifulSoup(str(subTitle), 'lxml')
    subTitle = soup.get_text()
    return subTitle


# Helper function, finds the release date of the alert
# returns the release date of the alert as a string ( Ex. feb 20, 2020 )
def getAlertReleaseDate(header):
    releaseDate = header.find('div', attrs={
        'class': 'submitted meta-text'}).text.encode('utf-8')
    dateArray = releaseDate.split()
    bMonth = dateArray[3]
    bDay = dateArray[4]
    bYear = dateArray[5]
    bMonthArray = str(bMonth).split("'")
    bDayArray = str(bDay).split("'")
    bYearArray = str(bYear).split("'")
    strMonth = bMonthArray[1]
    strDay = bDayArray[1]
    Day = strDay.split(',') #['18','']
    strYear = bYearArray[1] #2020
    dash = '-' # used to spearatce each part of the date
    strDate = strYear + dash + strMonth + dash + Day[0] #2020-January-18
    date = datetime.datetime.strptime(strDate, '%Y-%B-%d')
    cur = datetime.datetime.now()
    datetime_object = datetime.datetime(date.year, date.month, date.day, cur.hour, cur.minute, cur.second)
    return datetime_object


# Helper function, finds the  section that holds the summary of the alert
# then finds the field for the summary text
# returns the summary of the alert
def getSummary(content):
    article = content.find('article', attrs={'role': 'article'})
    summaryField = article.find('div', attrs={
        'class': 'field field--name-body field--type-text-with-summary field--label-hidden field--item'})
    summary = '' # used to concatenate all the summarys into one big summary
    for info in summaryField.findAll('p'):  # loop that gets a paragraoh and stores it in the summaryList
        soup = BeautifulSoup(str(info), 'lxml')
        summary += soup.get_text()
    return summary


# This function is used to check if there was a new alert posted to the ncas  alert feed/page.
# It uses the pickle module to load and dump the alert object. This is the smae as serializing and deserializing
# a object to a file. This is used to save a objects state. If the alert in the ncasAlertSerialization file is the same as
# the alert made when running the program, then there was no new alert posted. they they are different, that is a new alert
# write the new alert to the file so it can use alert when running the program again. 
def checkIfNewAlert(ncasAlert):
    with open('ncasAlertSerialization','rb') as alert_saved_to_file:
        lastAlert = pickle.load(alert_saved_to_file)
        if lastAlert.getPageTitle().lower() == ncasAlert.getPageTitle().lower():
            alert_saved_to_file.close()
            return False
        else:
            with open('ncasAlertSerialization','wb') as alert_saved_to_file:
                pickle.dump(ncasAlert,alert_saved_to_file)
                alert_saved_to_file.close()
                return True


""" calling functions """
getAllOfAlerts(url)
ncasAlert = getRecentAlertInfo(listOfLinks[0])
