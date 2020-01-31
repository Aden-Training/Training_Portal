from flask import Flask, render_template, request, redirect, url_for, session
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def root():
    return render_template("index.html")


@app.route('/sendEmail', methods=["GET", "POST"])
def sendEmail():
    if request.method == "POST":
        emailAd = request.form['emailAddress']
        courseT = request.form['courseType']
        reqDay = request.form['requestedDay']

        makeEmail(emailAd, courseT, reqDay)

    return render_template("new.html")


def makeEmail(recEmail, courseT, reqDay):
    #Add the shit pls ross




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)