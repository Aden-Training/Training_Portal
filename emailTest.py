import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

#Enter your address
senderEmail = "devtestross@gmail.com"  
#Enter receiver address
receiverEmail = "Tylerpower1551@gmail.com"  
#Need to maybe store the hashed password in the databse to store it and not enter every time
password = "DevPw2020*" 
#Office Email for Andrew (change to andrew's point of contact)
officeEmail = "tpower1551@gmail.com"

#This info will be taken from the applicatoin
applicantName = "Ross"
requestedDay = "13th June"
courseT = "forklift"

message = MIMEMultipart("alternative")
message["Subject"] = "Application Confirmation"
message["From"] = senderEmail
message["To"] = receiverEmail

html = """\
    <html>
    <body>
        <p>Hi,<br>
            You requested training on {} for {}.
            Please wait for confirmation.
        </p>
    </body>
    </html>

""".format(requestedDay, courseT)

#Turn these into plain/html MIMEText objects
part1 = MIMEText(html, "html")

#Add HTML/plain-text parts to MIMEMultipart message
#The email client will try to render the last part first

message.attach(part1)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(senderEmail, password)
    server.sendmail(senderEmail, receiverEmail, message.as_string())


#Sends email to employer
message = MIMEMultipart("alternative")
message["Subject"] = "Application Notification"
message["From"] = senderEmail
message["To"] = officeEmail

html = """\
    <html>
    <body>
        <p>Hi,<br>
            {} requested training on {} for {}.
            Please contact them to confirm this at {}.
        </p>
    </body>
    </html>

""".format(applicantName, requestedDay, courseT, receiverEmail)

part1 = MIMEText(html, "html")
message.attach(part1)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(senderEmail, password)
    server.sendmail(senderEmail, officeEmail, message.as_string())