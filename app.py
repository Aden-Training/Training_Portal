from flask import Flask, render_template, url_for, request, redirect, session, flash, send_file
from functools import wraps
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sqlite3
import bcrypt
import random
import smtplib, ssl
import os

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "lmaosecretkeylmao"

#   AUTHENTICATION

def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        busstatus = session.get('bus_logged_in', False)
        if not status:
            return redirect(url_for('.login', next=request.path))
        return f(*args, **kwargs)
    return decorated

def requires_bus_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        busstatus = session.get('bus_logged_in', False)
        if not busstatus:
            return redirect(url_for('.loginbus', next=request.path))
        return f(*args, **kwargs)
    return decorated

# Connect to the database
conn = sqlite3.connect("db/database.db")

# Create tables
conn.execute("CREATE TABLE IF NOT EXISTS customers (email TEXT UNIQUE, username TEXT, password TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS certificates(email TEXT, username TEXT, certificate TEXT, path TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS businesses (email TEXT, username TEXT, password TEXT, industry TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS courses (course_name TEXT, description TEXT, catagory TEXT, thumbnail TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS bookings (course_name TEXT, person_booked TEXT, persons_email TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS businessEmployees (company_name TEXT, employees TEXT)")

#   CUSTOMER PAGES

@app.route('/')
@requires_login
def root():
    return render_template("index.html")
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#   BUSINESS PAGES

@app.route('/businesstraining')
@requires_bus_login
def bustraining():
    return render_template('businessTraining.html')

#   COURSE HANDLING

# @app.route('/postcourse', methods = ["GET","POST"])
# def postcourse():
#     if request.method == "POST":

#         business = session['user']
#         name = request.form['courseName']
#         desc = request.form['courseDescription']

#         with sqlite3.connect('db/database.db') as con:
#             con.execute("INSERT INTO courses VALUES (?,?,?)", (business, name, desc))
    
#     return redirect('/businesstraining')

# ADMINISTRATION FEATURES
# POST A COURSE

@app.route('/postcourses', methods = ["POST","GET"])
def postcourses():
    if request.method == "POST":

        f = request.files['imageFile']
        name = request.form['courseTitle']
        desc = request.form['courseDescription']
        cat = request.form['courseCat']
        #thumb = request.form['imageFile']

        path = 'static/img/' + name + '.jpg'
        f.save('static/img/' + name +'.jpg')

        with sqlite3.connect('db/database.db') as con:
            con.execute("INSERT INTO courses VALUES (?,?,?,?)", (name, desc, cat, path))
    
        return redirect('/findcourse')

    return render_template('postcourse.html')

# COURSES AVAILABLE

@app.route('/courses', methods=["GET"])
def courses():
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    catagory = "Offshore"

    cur.execute("SELECT * FROM courses WHERE catagory = ?",[catagory])

    courses = cur.fetchall()

    return render_template('courses.html', courses = courses)

# REMOVE A COURSE

@app.route('/removecourse/<id>', methods=["GET", "POST"])
def removecourse(id):
    if request.method == "POST":
        with sqlite3.connect('db/database.db') as con:
            con.execute("DELETE FROM courses WHERE id = ?", [id])
            con.commit()

        return redirect('/courses')

# COURSES AVAILABLE

@app.route('/coursesavailable', methods=["GET"])
def coursesavailable():
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()

    return render_template('coursesavailable.html', courses = courses)

# FIND A COURSE

@app.route('/findcourse', methods=["GET", "POST"])
@requires_login
def findcourse():
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    catagory = "Offshore"

    cur.execute("SELECT * FROM courses WHERE catagory = ?",[catagory])
    course = cur.fetchall()

    return render_template('findcourse.html', course = course)

# INDIVIDUAL USER FUNCTIONALITY
# REGISTER AN INDIVIDUAL CUSTOMER

@app.route('/registercust', methods = ["GET","POST"])
def register():
    if request.method == "POST":
        with sqlite3.connect("db/database.db") as con:
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']

            passwd = password.encode('utf-8')
            hashedpw = bcrypt.hashpw(passwd, bcrypt.gensalt())

            con.execute("INSERT INTO customers VALUES(?,?,?)", (email, username, hashedpw))

            flash('You have now registered and can log in', 'success')
            status = session['logged_in'] = True
            session['user'] = request.form['username']

            os.mkdir('static/certificates/' + username +'/')

            return redirect('/')
    return render_template("register.html")

# LOGIN FOR AN INDIVIDUAL CUSTOMER

@app.route('/logincust', methods = ["GET","POST"])
def login():
    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']

        encodedpw = password.encode('utf-8')

        with sqlite3.connect("db/database.db") as con:
            cur = con.cursor()
            cur = con.execute("SELECT * FROM customers WHERE username = ?", [username])

            user = cur.fetchone()

            if cur != "":
                passwd = user[2]

                if(bcrypt.checkpw(encodedpw, passwd)):
                    status = session['logged_in'] = True
                    session['user'] = request.form['username']
                    flash('You have now logged into an account', 'success')
                    return redirect('/')
                else:
                    error = 'Invalid login'
                    return render_template('logincust.html', error=error)
            else:
                error = 'Username not found'
                return render_template('logincust.html', error=error)                
    return render_template("login.html")

# HOMEPAGE FOR INDIVIDUAL CUSTOMERS

@app.route('/customerHome', methods = ["GET"])
@requires_login
def customerHome():
    user = session['user']

    con = sqlite3.connect('db/database.db')
    conn = sqlite3.connect('db/database.db')

    conn.row_factory = sqlite3.Row
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    curs = conn.cursor()

    cur.execute("SELECT username FROM customers WHERE username = ?", [user])
    

    curs.execute("SELECT * FROM certificates WHERE username = ?", [user])
    certificates = curs.fetchall()

    customers = cur.fetchone()

    # Close Connection
    cur.close()
    curs.close()

    return render_template("customerHome.html", certificates = certificates, customers = customers)

@app.route('/downloadcertificate/<filename>', methods = ['POST'])
def downloadcert(filename):
    if request.method == "POST":
        con = sqlite3.connect('db/database.db')
        con.row_factory = sqlite3.Row

        cur = con.cursor()

        cur.execute("SELECT path FROM certificates WHERE certificate = ?", [filename])

        download = cur.fetchone()

    return send_file(download, attachment_filename="", as_attachment=True)




# BUSINESS ACCOUNT FUNCTIONALITY
# CREATE AN ACCOUNT IN BUSINESSES

@app.route('/registerbus', methods = ["GET","POST"])
def registerbus():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        industry = request.form['industry']

        passwd = password.encode('utf-8')

        hashpw = bcrypt.hashpw(passwd, bcrypt.gensalt())

        with sqlite3.connect("db/database.db") as con:
            con.execute("INSERT INTO businesses VALUES(?,?,?,?)",(email,username,hashpw,industry))

            busstatus = session['bus_logged_in'] = True
            session['user'] = request.form['username']

            return redirect('/businesstraining')

    return render_template("registerbus.html")

# LOGGING INTO A BUSINESS ACCOUNT

@app.route('/loginbus', methods = ["GET","POST"])
def loginbus():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        encodedpw = password.encode('utf-8')

        with sqlite3.connect("db/database.db") as con:
            cur = con.cursor()
            cur = con.execute("SELECT * FROM businesses WHERE username = ?", [username])

            user = cur.fetchone()

            if cur != "":
                passwd = user[2]

                if(bcrypt.checkpw(encodedpw, passwd)):
                    busstatus = session['bus_logged_in'] = True
                    session['user'] = request.form['username']
                    return redirect('/businesstraining')

    return render_template('loginbus.html')

# Creating an alternative bookcourse method

@app.route('/bookcourse/<coursename>', methods=["POST","GET"])
def bookcourse(coursename):
    if request.method == "POST":
        con = sqlite3.connect('db/database.db')
        cur = con.cursor()

        course = coursename
        user = session['user']

        cur.execute("SELECT * FROM customers WHERE username = ?",[user])

        cust_data = cur.fetchone()

        email = cust_data[0]

        with sqlite3.connect('db/database.db') as con:
            con.execute("INSERT INTO bookings VALUES (?,?,?)",(course,user,email))
            con.commit()

    flash("You're Successfully booked onto %s!" % course)

    return redirect('/findcourse')

@app.route('/peoplebooked/<coursename>', methods=["GET"])
def peoplebooked(coursename):
    con = sqlite3.connect('db/database.db')
    cur = con.cursor()

    cur.execute("SELECT person_booked FROM bookings WHERE course_name = ?", [coursename])

    people = cur.fetchall()

    return render_template('peoplebooked.html', people = people)


@app.route('/awardcertificate', methods=["GET", "POST"])
def awardcertificate():
    if request.method=="POST":
        
        email = request.form['recipiantEmail']

        con = sqlite3.connect('db/database.db')

        cur = con.cursor()

        cur = con.execute("SELECT username FROM customers WHERE email = ?",[email])

        username = cur.fetchone()[0]

        docName = request.form['docName']
        recipiantEmail = request.form['recipiantEmail']
        f = request.files['PDFfile']

        path = "static/certificates/" + username + "/" + docName + ".pdf"
        certificate = request.form['docName']

        with sqlite3.connect('db/database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT into certificates VALUES (?,?,?,?)",(email,username,certificate,path))

        f.save('static/certificates/' + username + '/' + docName + '.pdf')
        sendCertificate(recipiantEmail, path)
        return redirect('/customerHome')

    return render_template('awardcertificate.html')


def sendCertificate(recipiantEmail, pdf):
    subject = "Certificate for course completion"
    body = "Please find attached the certificate proving that you completed the course"
    sender_email = "devtestross@gmail.com"
    receiver_email = recipiantEmail
    password = "DevPw2020*"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    filename = pdf

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        "attachment; filename= {}".format(filename),
    )

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
