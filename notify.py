import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

current = datetime.datetime.now()
renew = current.minute + 3
print(renew)
print(current)

while(True):
    current = datetime.datetime.now()
    if current.minute == renew:
        print("Time to renew")

        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"

        senderEmail = "devtestross@gmail.com"  
        receiverEmail = "rosscameronclarkbell@gmail.com"  
        password = "DevPw2020*" 

        requestedDay = "13th June" #Will need to be taken from db or site etc
        courseT = "forklift" #Will need to be taken from db or site etc 

        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Renewal Date Soon!"
        message["From"] = senderEmail
        message["To"] = receiverEmail

        html = """\
            <html>
            <body>
                <p>Hi,<br>
                    Your certificate will need to be renewed on at {}mins past for {}. 
                    Please apply now to secure your spot.
                </p>
            </body>
            </html>
        """.format(renew, courseT)

        part1 = MIMEText(html, "html")
        message.attach(part1)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(senderEmail, password)
            server.sendmail(senderEmail, receiverEmail, message.as_string())

        break
