import datetime
import pandas as pd
from sendEmail import sendEmails

def constructEmail(email, cves, currentActivities, aptAlerts):
    includeCVE = False
    includeCA = False
    includeAPT = False

    
    #initializes all data as DataFrames
    pd.set_option('display.max_colwidth', 0)
    if(cves):
        includeCVE = True
        cvedf = pd.DataFrame(cves, columns=['Email', 'keys', 'CVE Number', 'Description', 'Impact Score V2', 'Impact Score V3', 'Published Date', 'Time_Received'])
        cvedf.drop(cvedf.columns[[0,1,6,7]], axis=1, inplace=True)
        cvedf["Link"] = 'https://nvd.nist.gov/vuln/detail/' + cvedf['CVE Number']
        htmlcvedf = cvedf.to_html(index=False,justify='center')
    
    if(currentActivities):
        includeCA = True
        cadf = pd.DataFrame(currentActivities, columns=['email', 'keys', 'Title', 'Published_Date', 'Description', 'Link'])
        cadf.drop(cadf.columns[[0,1,3]], axis=1, inplace=True)
        htmlcadf = cadf.to_html(index=False, justify='center')

    if(aptAlerts):
        includeAPT = True
        aptdf = pd.DataFrame(aptAlerts, columns=['email', 'keys', 'Alert Number', 'release_date', 'Title', 'Description'])
        aptdf.drop(aptdf.columns[[0,1,3]], axis=1, inplace=True)
        aptdf["Link"] = 'https://www.us-cert.gov/ncas/alerts/' + aptdf['Alert Number']
        htmlaptdf = aptdf.to_html(index=False, justify='center')
   #deletes unnecessary column from tables
   # cvedf.drop(cvedf.columns[[0,1,6,7]], axis=1, inplace=True)
   # cadf.drop(cadf.columns[[0,1,3]], axis=1, inplace=True)
   # aptdf.drop(aptdf.columns[[0,1,3]], axis=1, inplace=True)

    #adds final column to CVE table
    #cvedf["Link"] = 'https://nvd.nist.gov/vuln/detail/' + cvedf['CVE Number']
   # aptdf["Link"] = 'https://www.us-cert.gov/ncas/alerts/' + aptdf['Alert Number']


    #converts all DataFrames to HTML Tables
    #htmlcvedf = cvedf.to_html(index=False,justify='center')
   # htmlcadf = cadf.to_html(index=False, justify='center')
   # htmlaptdf = aptdf.to_html(index=False, justify='center')

    #initializes all other necessary HTML Objects for email
    image1 = '<p style="text-align:center;"><img src="https://i.ibb.co/8Yz3QYS/Screen-Shot-2020-04-08-at-1-06-59-AM.png" alt="VAST_LOGO" style="width:370px;height:140px;"></p>'
    heading1 = '<h1>CVE Alerts</h1>'
    heading2 = '<h1><br>NCAS Current Activity Feed</h1>'
    heading3 = '<h1><br>NCAS Alerts</h1>'
    heading4 = '<h2><br>No applicable alerts</h2>'

   #creates body of email
    list_of_html_objects= [image1]
    data= False

    if(includeCVE):
        list_of_html_objects.append(heading1)
        list_of_html_objects.append(htmlcvedf)
        data = True
    if(includeCA):
        list_of_html_objects.append(heading2)
        list_of_html_objects.append(htmlcadf)
        data = True
    if(includeAPT):
        list_of_html_objects.append(heading3)
        list_of_html_objects.append(htmlaptdf)
        data = True
   # if(not data):
   #     list_of_html_objects.append(heading4)


    bodyString = '\n\n'.join(list_of_html_objects)


    #sends email
    if(data):
        sendEmails(email, bodyString)

