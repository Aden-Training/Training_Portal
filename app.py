from flask import Flask, render_template, url_for, request, redirect, session, flash
from functools import wraps
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sqlite3
import bcrypt
import random
import smtplib, ssl

app = Flask(__name__)
app.secret_key = "lmaosecretkeylmao"

#   Authentication Middleware
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

conn = sqlite3.connect("db/database.db")

conn.execute("CREATE TABLE IF NOT EXISTS customers (username TEXT, password TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS businesses (username TEXT, password TEXT, industry TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, business TEXT, course_name TEXT, description TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS bookings (person_booked TEXT, course_name TEXT)")

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

@app.route('/postcourse', methods = ["GET","POST"])
def postcourse():
    if request.method == "POST":

        business = session['user']
        name = request.form['courseName']
        desc = request.form['courseDescription']

        with sqlite3.connect('db/database.db') as con:
            con.execute("INSERT INTO courses VALUES (null,?,?,?)", (business, name, desc))
    
    return redirect('/businesstraining')

@app.route('/postcourses')
def postcourses():
    return render_template('postcourse.html')

@app.route('/courses', methods=["GET"])
def courses():
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("SELECT * FROM courses WHERE business = ?", [session['user']])
    courses = cur.fetchall()

    return render_template('courses.html', courses = courses)

#   LOGGING IN CUSTOMERS

@app.route('/coursesavailable', methods=["GET"])
def coursesavailable():
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()

    return render_template('coursesavailable.html', courses = courses)


@app.route('/registercust', methods = ["GET","POST"])
def register():
    if request.method == "POST":
        with sqlite3.connect("db/database.db") as con:
            username = request.form['username']
            password = request.form['password']

            passwd = password.encode('utf-8')
            hashedpw = bcrypt.hashpw(passwd, bcrypt.gensalt())

            con.execute("INSERT INTO customers VALUES(?,?)", (username, hashedpw))

            status = session['logged_in'] = True
            session['user'] = request.form['username']

            return redirect('/')

    return render_template("register.html")

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
                passwd = user[1]

                if(bcrypt.checkpw(encodedpw, passwd)):
                    status = session['logged_in'] = True
                    session['user'] = request.form['username']
                    return redirect('/')
    return render_template("login.html")

#   LOGGING IN businesses
@app.route('/registerbus', methods = ["GET","POST"])
def registerbus():
    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        industry = request.form['industry']

        passwd = password.encode('utf-8')

        hashpw = bcrypt.hashpw(passwd, bcrypt.gensalt())

        with sqlite3.connect("db/database.db") as con:
            con.execute("INSERT INTO businesses VALUES(?,?,?)",(username,hashpw,industry))

            busstatus = session['bus_logged_in'] = True
            session['user'] = request.form['username']

            return redirect('/businesstraining')

    return render_template("registerbus.html")

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
                passwd = user[1]

                if(bcrypt.checkpw(encodedpw, passwd)):
                    busstatus = session['bus_logged_in'] = True
                    session['user'] = request.form['username']
                    return redirect('/businesstraining')

    return render_template('loginbus.html')


@app.route('/removecourse/<id>', methods=["GET", "POST"])
def removecourse(id):
    if request.method == "POST":
        with sqlite3.connect('db/database.db') as con:
            con.execute("DELETE FROM courses WHERE id = ?", [id])
            con.commit()

        return redirect('/courses')

@app.route('/bookcourse/<coursename>', methods=["POST","GET"])
def bookcourse(coursename):
    if request.method == "POST":

        course = coursename
        user = session['user']


        with sqlite3.connect('db/database.db') as con:
            con.execute("INSERT INTO bookings VALUES (?,?)",(user,course))
            con.commit()

    flash("You're Successfully booked onto %s!" % course)

    return redirect('/coursesavailable')

@app.route('/peoplebooked/<coursename>', methods=["GET"])
def peoplebooked(coursename):
    con = sqlite3.connect('db/database.db')
    cur = con.cursor()

    cur.execute("SELECT person_booked FROM bookings WHERE course_name = ?", [coursename])

    people = cur.fetchall()

    return render_template('peoplebooked.html', people = people)



# @app.route('/')
# def root():
#     return render_template("index.html")


# @app.route('/sendEmail', methods=["GET", "POST"])
# def sendEmail():
#     if request.method == "POST":
#         emailAd = request.form['emailAddress']
#         courseT = request.form['courseType']
#         reqDay = request.form['requestedDay']

#         makeEmail(emailAd, courseT, reqDay)

#     return render_template("new.html")


# def makeEmail(recEmail, courseT, reqDay):
#     #Add the shit pls ross

#Ross's stuff, can remove later
@app.route('/findcourse', methods=["GET", "POST"])
def findcourse():
    return render_template('findcourse.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
