from flask import Flask, render_template, url_for, request, redirect, session, flash, send_file, send_from_directory
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

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        adminstatus = session.get('admin_logged_in', False)
        if not adminstatus:
            return redirect(url_for('.loginadmin', next=request.path))
        return f(*args, **kwargs)
    return decorated
conn = sqlite3.connect("db/database.db")

# Create tables
conn.execute("CREATE TABLE IF NOT EXISTS customers (email TEXT UNIQUE, username TEXT, password TEXT, organisation TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS certificates(email TEXT, username TEXT, certificate TEXT, path TEXT, organisation TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS businesses (email TEXT, username TEXT, password TEXT, industry TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, course_name TEXT, description TEXT, category TEXT, thumbnail TEXT, subCat TEXT, org TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS bookings (course_name TEXT, person_booked TEXT, persons_email TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS businessEmployees (company_name TEXT, employees TEXT)")

conn.execute("CREATE TABLE IF NOT EXISTS admin (email TEXT, username TEXT, password TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS employees (email TEXT, username TEXT, org TEXT)")


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

# ADMINISTRATION FEATURES
# POST A COURSE

@app.route('/postcourses', methods = ["POST","GET"])
@requires_admin
def postcourses():
    if request.method == "POST":

        f = request.files['imageFile']
        org = request.form['org']
        name = request.form['courseTitle']
        desc = request.form['courseDescription']
        category = request.form['courseCat']
        subCategory = request.form['subCourseCat']

        path = 'static/img/' + name + '.jpg'
        f.save('static/img/' + name +'.jpg')

        cat = detectCat(category)

        if(cat == "SafetyTraining" or cat == "WorkshopSkills"):
            subCat = detectSubCat(subCategory)
        else:
            subCat = "Null"

        with sqlite3.connect('db/database.db') as con:
            con.execute("INSERT INTO courses VALUES (NULL,?,?,?,?,?,?)", (name, desc, cat, path, subCat, org))
    
        return redirect('/adminpage')

    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("SELECT * FROM businesses")

    companies = cur.fetchall()

    return render_template('postcourse.html', companies = companies)

# REMOVE A COURSE

@app.route('/removecourses')
def removecourses():
        con = sqlite3.connect('db/database.db')
        con.row_factory = sqlite3.Row

        cur = con.cursor()

        cur.execute("SELECT * FROM courses")

        courses = cur.fetchall()

        return render_template('removecourses.html', courses = courses)

@app.route('/removecourse/<id>', methods=["POST"])
def removecourse(id):
    if request.method == "POST":
        with sqlite3.connect('db/database.db') as con:
            con.execute("DELETE FROM courses WHERE id = ?", [id])
            con.commit()
    return redirect('/removecourses')

# FIND A COURSE
@app.route('/findcourse')
@requires_login
def findcourses():
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    category = "SafetyTraining"

    cur.execute("SELECT * FROM courses")
    course = cur.fetchall()

    return render_template('findcourse.html', course = course)

@app.route('/<category>', methods=["GET", "POST"])
@requires_login
def findcourse(category):
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    # category = "Offshore"

    catList = ["SafetyTraining", "ForkliftAndPlant", "FirstAid", "WorkshopSkills", "BespokeTraining", "Other"]
    subCatList = ["FireTraining", "WorkingAtHeight", "ConfinedSpace", "LiftingOperations", "Environmental", "General", "MechanicalJoint"]

    for i in catList:
        if(i == category):
            cur.execute("SELECT * FROM courses WHERE category = ?",[category])
    
    for i in subCatList:
        if(i == category):
            cur.execute("SELECT * FROM courses WHERE subCat = ?",[category])
    
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

            con.execute("INSERT INTO customers VALUES(?,?,?,NULL)", (email, username, hashedpw))

            flash('You have now registered and can log in', 'success')
            status = session['logged_in'] = True
            session['user'] = request.form['username']
            session['email'] = request.form['email']

            os.mkdir('static/certificates/' + username +'/')

            return redirect('/customerHome')
    return render_template("register.html")

# LOGIN FOR AN INDIVIDUAL CUSTOMER

@app.route('/logincust', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        session.clear()
        username = request.form['username']
        password = request.form['password']

        encodedpw = password.encode('utf-8')

        with sqlite3.connect("db/database.db") as con:
            cur = con.cursor()
            cur = con.execute("SELECT * FROM customers WHERE username = ?", [username])

            user = cur.fetchone()

            if cur != "":
                try:
                    passwd = user[2]

                    if(bcrypt.checkpw(encodedpw, passwd)):
                        status = session['logged_in'] = True
                        session['user'] = request.form['username']
                        flash('You have now logged into an account', 'success')
                        return redirect('/customerHome')
                except:
                    passerror = 'Invalid login'

                    return render_template('login.html', error = passerror)  
                else:  
                    error = 'Username not found'
                    return render_template('login.html', error = error)
              
    return render_template("login.html")

# HOMEPAGE FOR INDIVIDUAL CUSTOMERS

@app.route('/customerHome', methods = ["GET"])
@requires_login
def customerHome():
    user = session['user']

    con = sqlite3.connect('db/database.db')
    conn = sqlite3.connect('db/database.db')
    connn = sqlite3.connect('db/database.db')

    connn.row_factory = sqlite3.Row
    conn.row_factory = sqlite3.Row
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    curs = conn.cursor()
    cursor = connn.cursor()

    cur.execute("SELECT * FROM customers WHERE username = ?", [user])
    

    curs.execute("SELECT * FROM certificates WHERE username = ?", [user])
    cursor.execute("SELECT * FROM bookings WHERE person_booked = ?", [user])

    courses = cursor.fetchall()
    certificates = curs.fetchall()

    customers = cur.fetchone()

    # Close Connection
    cur.close()
    curs.close()
    cursor.close()
    
    return render_template("customerHome.html", certificates = certificates, customers = customers, courses=courses)

@app.route('/downloadcertificate/<filename>', methods = ['POST','GET'])
def downloadcert(filename):
    if request.method == "POST":
        con = sqlite3.connect('db/database.db')
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        filename = filename
        cur.execute("SELECT path FROM certificates WHERE certificate = ?", [filename])

        # filename = filename + '.pdf'
        download = cur.fetchone()
        # look in [Username]/[Filename]

        directory = 'static/certificates/' + session['user'] + '/' + filename

        return send_file(directory, attachment_filename=filename)
    else:
        return redirect('/customerHome')




# BUSINESS ACCOUNT FUNCTIONALITY
# CREATE AN ACCOUNT IN BUSINESSES

@app.route('/registerbus', methods = ["GET","POST"])
@requires_admin
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

            return redirect('/adminpage')

    return render_template("registerbus.html")

# LOGGING INTO A BUSINESS ACCOUNT

@app.route('/loginbus', methods = ["GET","POST"])
def loginbus():
    if request.method == "POST":
        session.clear()
        username = request.form['username']
        password = request.form['password']

        encodedpw = password.encode('utf-8')

        with sqlite3.connect("db/database.db") as con:
            cur = con.cursor()
            cur = con.execute("SELECT * FROM businesses WHERE username = ?", [username])

            user = cur.fetchone()

            if cur != "":
                try:
                    passwd = user[2]

                    if(bcrypt.checkpw(encodedpw, passwd)):
                        busstatus = session['bus_logged_in'] = True
                        session['user'] = request.form['username']
                        return redirect('/businesstraining')
                except:
                    passerror = 'Invalid login'

                    return render_template('login.html', error = passerror)  
                else:  
                    error = 'Username not found'
                    return render_template('login.html', error = error)
            
    return render_template('loginbus.html')

# Login admin
@app.route('/loginadmin', methods=["GET","POST"])
def loginadmin():
    if request.method == "POST":
        session.clear()
        username = request.form['username']
        password = request.form['password']

        encodedpw = password.encode('utf-8')

        with sqlite3.connect("db/database.db") as con:
            cur = con.cursor()
            cur = con.execute("SELECT * FROM admin WHERE username = ?", [username])

            user = cur.fetchone()

            if cur != "":
                try:
                    passwd = user[2]
                    adminstatus = session['admin_logged_in'] = True
                    session['user'] = request.form['username']
                    return redirect('/adminpage')
                except:
                    passerror = 'Invalid login'

                    return render_template('login.html', error = passerror)  
                else:  
                    error = 'Username not found'
                    return render_template('login.html', error = error)
            
    return render_template('adminlogin.html')

@app.route('/adminpage', methods=["GET"])
@requires_admin
def adminpage():
    return render_template('adminhome.html')

# Creating an alternative bookcourse method

@app.route('/bookcourse/<coursename>', methods=["POST","GET"])
def bookcourse(coursename):
    if request.method == "POST":
        con = sqlite3.connect('db/database.db')
        # con.row_factory = sqlite3.Row

        cur = con.cursor()
        curs = con.cursor()

        course = coursename
        user = session['user']

        cur.execute("SELECT * FROM customers WHERE username = ?",[user])
        curs.execute("SELECT email FROM admin WHERE username = 'andy'")

        adminemail = curs.fetchone()

        cust_data = cur.fetchone()

        email = cust_data[0]

        with sqlite3.connect('db/database.db') as con:
            con.execute("INSERT INTO bookings VALUES (?,?,?)",(course,user,email))
            con.commit()
        
        aEmail = str(adminemail)
        aLen = len(aEmail) - 3
        aEmail = aEmail[2:aLen]

        try:
            sendConfirmation(coursename, email, user)
            sendConfirmationOffice(coursename, email, user, aEmail)
            return redirect('/customerHome')
        except:
            return redirect('/customerHome')

        flash("You're Successfully booked onto %s! Email confirmation has been sent." % course)

    return redirect('/findcourse')

@app.route('/peoplebooked/<coursename>', methods=["GET"])
def peoplebooked(coursename):
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("SELECT * FROM bookings WHERE course_name = ?", [coursename])

    people = cur.fetchall()

    return render_template('peoplebooked.html', people = people)


@app.route('/awardcertificate', methods=["GET", "POST"])
@requires_admin
def awardcertificate():
    if request.method=="POST":
        
        email = request.form['recipiantEmail']
        organisation = request.form['company']

        con = sqlite3.connect('db/database.db')

        cur = con.cursor()

        cur = con.execute("SELECT username FROM customers WHERE email = ?",[email])

        username = cur.fetchone()[0]

        docName = request.form['docName']
        f = request.files['PDFfile']

        path = "static/certificates/" + username
        certificate = request.form['docName']

        with sqlite3.connect('db/database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT into certificates VALUES (?,?,?,?,?)",(email,username,certificate,path, organisation))

        f.save('static/certificates/' + username + '/' + docName + '.pdf')
        # sendCertificate(recipiantEmail, path)
        
        return redirect('/adminpage')
    else:
        con = sqlite3.connect('db/database.db')
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        curs = con.cursor()

        cur.execute("SELECT * FROM customers")
        curs.execute("SELECT * FROM businesses")

        companies = curs.fetchall()
        customers = cur.fetchall()

        return render_template('awardcertificate.html', customers = customers, companies = companies)


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

def sendConfirmation(course, recipiantEmail, recipiantName):
    port = 465
    smtp_server = "smtp.gmail.com"

    #Email to cusotmer
    senderEmail = "devtestross@gmail.com"
    password = "DevPw2020*"
    #officeEmail = "40317736@live.napier.ac.uk"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Application Awaiting Confirmation"
    message["From"] = senderEmail
    message["To"] = recipiantEmail

    html = """\
        <html>
        <body>
            <p>Hi {},<br>
                You requested training for {}.
                Please wait for confirmation.
            </p>
        </body>
        </html>
    """.format(recipiantName, course)

    part1 = MIMEText(html, "html")
    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(senderEmail, password)
        server.sendmail(senderEmail, recipiantEmail, message.as_string())


def sendConfirmationOffice(course, recipiantEmail, recipiantName, officeEmail):
    #Email to office
    port = 465
    smtp_server = "smtp.gmail.com"

    #Email to cusotmer
    senderEmail = "devtestross@gmail.com"
    password = "DevPw2020*"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Application Notification"
    message["From"] = senderEmail
    message["To"] = officeEmail

    html = """\
        <html>
        <body>
            <p>Hi, <br>
                {} requested training for {}.
                Please contact them to confirm this at {}.
            </p>
        </body>
        </html>
    """.format(recipiantName, course, recipiantEmail)

    part1 = MIMEText(html, "html")
    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(senderEmail, password)
        server.sendmail(senderEmail, officeEmail, message.as_string())


def detectCat(category):
    if(category =="Safety"):
        catNew = "SafetyTraining"
    elif(category =="Forklift and Plant"):
        catNew = "ForkliftAndPlant"
    elif(category =="First Aid"):
        catNew = "FirstAid"
    elif(category == "Workshop"):
        catNew = "WorkshopSkills"
    elif(category == "BESPOKE Training"):
        catNew = "BespokeTraining"
    elif(category == "Other"):
        catNew = "Other"
    else:
        catNew = "ERROR"

    return catNew

def detectSubCat(subCategory):
    if(subCategory == "Fire Training"):
        subCatNew = "FireTraining"
    elif(subCategory == "Working at Height"):
        subCatNew = "WorkingAtHeight"
    elif(subCategory == "Confined Space"):
        subCatNew = "ConfinedSpace"
    elif(subCategory == "Lifting Operations"):
        subCatNew = "Lifting Operations"
    elif(subCategory == "Environmental"):
        subCatNew = "Environmental"
    elif(subCategory == "General"):
        subCatNew = "General"
    elif(subCategory == "Mechanical Joint"):
        subCatNew = "MechanicalJoint"
    else:
        subCatNew = "ERROR"
    
    return subCatNew

@app.route('/courses')
@requires_bus_login
def courses():
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("SELECT * FROM courses WHERE org = ?", [session['user']])

    courses = cur.fetchall()

    return render_template('courses.html', courses = courses)


@app.route('/changepassword', methods = ["GET","POST"])
def changepass():
    if request.method == "POST":
        user = session['user']
        password = request.form['newpass']

        password = password.encode('utf-8')
        passhash = bcrypt.hashpw(password, bcrypt.gensalt())

        with sqlite3.connect('db/database.db') as con:
            con.execute("UPDATE customers SET password = ? WHERE username = ?", (passhash, session['user']))
            con.execute("UPDATE businesses SET password = ? WHERE username = ?", (passhash, session['user']))
            con.execute("UPDATE admin SET password = ? WHERE username = ?", (passhash, session['user']))
        msg = "Password successfully changed!"

        return redirect('/customerHome')
    else:
        return render_template('changepass.html')

@app.route('/changeemail', methods = ["GET","POST"])
def changeemail():
    if request.method == "POST":
        user = session['user']
        email = request.form['newemail']

        email = email.encode('utf-8')

        with sqlite3.connect('db/database.db') as con:
            con.execute("UPDATE customers SET email = ? WHERE username = ?", (email, session['user']))
            con.execute("UPDATE businesses SET email = ? WHERE username = ?", (email, session['user']))
            con.execute("UPDATE admin SET email = ? WHERE username = ?", (email, session['user']))
        msg = "Email successfully changed!"

        return redirect('/customerHome')
    else:
        return render_template('changeemail.html')

@app.route('/listemployees', methods = ["GET"])
def listemployees():
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("SELECT * FROM employees WHERE org = ?", [session['user']])

    employees = cur.fetchall()

    return render_template('employees.html', employees = employees)


@app.route('/employeecert/<username>')
@requires_bus_login
def employeecert(username):
    con = sqlite3.connect('db/database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("SELECT * FROM certificates WHERE username = ? AND organisation = ?", [username, session['user']])

    certs = cur.fetchall()

    return render_template('employeecert.html', certs = certs)

@app.route('/addemployeeform', methods = ["GET","POST"])
def addemployees():
    if request.method=="POST":
        email = request.form['email']
        username = request.form['username']
        org = session['user']

        con = sqlite3.connect('db/database.db')

        cur = con.cursor()

        cur.execute("SELECT * FROM customers WHERE username = ?", [username])
        con.close()
        if cur != "":
            with sqlite3.connect("db/database.db") as conn:
                conn.execute("INSERT INTO employees VALUES(?,?,?)", (email, username, org))
                conn.execute("UPDATE customers SET organisation = ? WHERE email = ?", (org, email) )
            return redirect('/listemployees')
        else:
            return render_template('addemployees.html')
    
    else:
        con = sqlite3.connect('db/database.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute("SELECT * FROM customers")

        customer = cur.fetchall()

        return render_template('addemployees.html', customer = customer)

@app.route('/removeemployee', methods = ["GET","POST"])
def removemployee():
    if request.method=="POST":
        # email = request.form['email']
        username = request.form['username']
        org = session['user']

        con = sqlite3.connect('db/database.db')

        cur = con.cursor()

        cur.execute("SELECT * FROM customers WHERE username = ? AND organisation = ?", [username, session['user']])
        con.close()

        if cur != "":
            with sqlite3.connect("db/database.db") as conn:
                conn.execute("DELETE FROM employees WHERE username = ? AND org = ?", [username, session['user']])
                conn.execute("UPDATE customers SET organisation = NULL WHERE username = ?", [username])
            return redirect('/listemployees')
        else:
            return render_template('removeemployee.html')
    
    else:
        con = sqlite3.connect('db/database.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM employees WHERE org = ?", [session['user']])

        employees = cur.fetchall()

        return render_template('removeemployee.html', employees = employees)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)