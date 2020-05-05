import pymysql
import mysql.connector
import ParseJsonFile
import datetime
from constructEmail import constructEmail

# The main process for the notification part of the program
# Method connects to database, grabs all users, checks their Time Recieved
# checks their Frequency, grabs all alerts for the user, and sends email. 
def grabFromDatabase():
    try:
        cnx = mysql.connector.connect(user='cyberuser', password='cyber',
                host='127.0.0.1',
                database='VAST')
        cursor = cnx.cursor(buffered=True)

        selectAllUsersQuery = "select user_id, Email, Frequency, Time_Received from User_Data"
        
        updateTime_RecievedQuery = """ UPDATE User_Data SET Time_Received = %s WHERE user_id = %s """
        
        selectCvesQuery = """ SELECT ud.Email, k.keys, c.CVE_Number, c.description, c.impactV2, c.impactV3, c.Published_Date, ud.Time_Received \
                FROM User_Data ud \
                JOIN User_Keyword uk on uk.user_id = ud.user_id \
                JOIN Keyword k on k.keyword_id = uk.keyword_id \
                JOIN CVE_Alerts c on c.keyword_id = k.keyword_id\
                WHERE ud.Email = %s\
                AND c.Published_Date > ud.Time_Received\
                OR c.Published_Date =  ud.Time_Received """
        
        selectCurrentActivitiesQuery = """ SELECT ud.email, k.keys, ca.Title, ca.Published_Date, ca.Description, ca.Relevant_Link\
                FROM User_Data ud\
                JOIN User_Keyword uk on uk.user_id = ud.user_id\
                JOIN Keyword k on k.keyword_id = uk.keyword_id\
                JOIN Current_Activities ca on ca.Keyword_id = k.Keyword_id\
                WHERE ud.user_id = %s\
                AND ca.Published_Date > ud.Time_Received\
                OR ca.Published_Date = ud.Time_Received """

        selectAPT_Alerts = """ SELECT ud.email, k.keys, aa.alert_number, aa.release_date, aa.alert_title, aa.description\
                FROM User_Data ud\
                JOIN User_Keyword uk on uk.user_id = ud.user_id\
                JOIN Keyword k on k.keyword_id = uk.keyword_id\
                JOIN APT_Alerts aa on aa.keyword_id = k.keyword_id\
                WHERE ud.user_id = %s\
                AND aa.release_date > ud.Time_Received\
                OR aa.release_date = ud.Time_Received """        
        
        
        
        cursor.execute("USE VAST")
        cursor.execute(selectAllUsersQuery)
        users = cursor.fetchall()

        for user in users:
            user_id = user[0] # int
            email = user[1] # String
            frequency = int(user[2]) # int
            time_Received = user[3] # datetime.datetime object
            diff = ParseJsonFile.current_time_when_program_runs  - time_Received # Ex. 2020-03-27 02:30:45 - 2020-03-26 23:25:36 = 3:05:09
            diffInHours = getDiffInHours(diff)

            if time_Received.hour == 0:
                # grab all the alerts
                qvalues=(email,)
                cursor.execute(selectCvesQuery,qvalues) 
                cves = cursor.fetchall() # list of cves
                
                qvalues=(user_id,)
                cursor.execute(selectCurrentActivitiesQuery,qvalues) 
                currentActivities = cursor.fetchall() # list of current activities 
                
                cursor.execute(selectAPT_Alerts,qvalues) 
                aptAlerts = cursor.fetchall() # list of apt alerts

                # send email method that takes in a email, list of cves, list of current Activites, and list of aptAlerts
                constructEmail(email, cves, currentActivities, aptAlerts)

                #sets Time_received to current_time_when_program_runs
                newTime_RecievedData = (currentDateTimeFormate(), user_id)
                cursor.execute(updateTime_RecievedQuery, newTime_RecievedData)
                cnx.commit()

                
            elif diffInHours >= frequency:
                # grab all the alerts
                qvalues=(email,)
                cursor.execute(selectCvesQuery,qvalues) 
                cves = cursor.fetchall() # list of cves
                 
                qvalues=(user_id,)
                cursor.execute(selectCurrentActivitiesQuery,qvalues) 
                currentActivities = cursor.fetchall() # list of current activities 
                
                cursor.execute(selectAPT_Alerts,qvalues) 
                aptAlerts = cursor.fetchall() # list of apt alerts

                # send email method that takes in a email, list of cves, list of current Activites, and list of aptAlerts
                constructEmail(email, cves, currentActivities, aptAlerts)
                #print('sending email to' + email)
                
                #sets Time_received to current_time_when_program_runs
                newTime_RecievedData = (currentDateTimeFormate(), user_id)
                cursor.execute(updateTime_RecievedQuery, newTime_RecievedData)
                cnx.commit()

    
    except mysql.connector.Error as error:
        #print("Failed to insert record into CVE table {}".format(error))
        print(error)
        print(type(error))


# Returns a dateTime object from the current time when program runs
# without microseconds. Ex 2020-03-25 13:04:30
def currentDateTimeFormate():
    dateArr = str(ParseJsonFile.current_time_when_program_runs).split('.')
    strDate = dateArr[0]
    dateTime_object = datetime.datetime.strptime(strDate, '%Y-%m-%d %H:%M:%S')
    return dateTime_object

# Returns the hours of a time delta object. 
def getDiffInHours(diff):
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    return hours

