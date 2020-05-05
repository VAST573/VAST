import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
# set up the SMTP server

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "vulnerabilityalertsystemtool@gmail.com"
password = "mansary!"

#Initalizes connection to SMTP server, logs into sender email, sends emails 
def sendEmails(receiver_email, html):
    print('sending email')
    #receiver_email = 'alexabbott42@gmail.com'
    message = MIMEMultipart("alternative")
    message["Subject"] = "VAST Alerts for " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
            plain text html failed"""
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server,port)
        server.starttls(context=context) 
        server.login(sender_email, password)

        
        server.sendmail(sender_email,receiver_email, message.as_string())
        print("Sent email to " + receiver_email)
    
    except Exception as e:
        print(e)
    finally:
       server.quit()

