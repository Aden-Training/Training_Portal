from flask import Flask, render_template, url_for, request, redirect, session, flash
from functools import wraps
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#import sqlite3
#import bcrypt
import random
import smtplib, ssl

app = Flask(__name__)
#app.secret_key = "lmaosecretkeylmao"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'adentraining'
app.config['MYSQL_DB'] = 'DictCursor'

#init MYSQL
mysql= MySQL(app)


# Authentication Middleware
#def requires_login(f):
    #@wraps(f)
    #def decorated(*args, **kwargs):
     #   status = session.get('logged_in', False)
      #  busstatus = session.get('bus_logged_in', False)
       # if not status:
        #    return redirect(url_for('.login', next=request.path))
       # return f(*args, **kwargs)
   # return decorated

#def requires_bus_login(f):
 #   @wraps(f)
  #  def decorated(*args, **kwargs):
   #     busstatus = session.get('bus_logged_in', False)
    #    if not busstatus:
     #       return redirect(url_for('.loginbus', next=request.path))
      #  return f(*args, **kwargs)
   # return decorated

#conn = sqlite3.connect("db/database.db")

#conn.execute("CREATE TABLE IF NOT EXISTS customers (email TEXT, username TEXT, password TEXT)")
#conn.execute("CREATE TABLE IF NOT EXISTS businesses (email TEXT, username TEXT, password TEXT, industry TEXT)")
#conn.execute("CREATE TABLE IF NOT EXISTS courses (course_name TEXT, description TEXT, catagory TEXT, thumbnail TEXT)")
#conn.execute("CREATE TABLE IF NOT EXISTS bookings (course_name TEXT, person_booked TEXT, persons_email TEXT)")

#   CUSTOMER PAGES

#@app.route('/')
@requires_login
def root():
    return render_template("index.html")
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#   BUSINESS PAGES

#@app.route('/businesstraining')
#@requires_bus_login
#def bustraining():
 #   return render_template('businessTraining.html')

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

#@app.route('/postcourses', methods = ["POST","GET"])
#def postcourses():
 #   if request.method == "POST":

  #      f = request.files['imageFile']
   #     name = request.form['courseTitle']
    #    desc = request.form['courseDescription']
     #   cat = request.form['courseCat']
        #thumb = request.form['imageFile']

     #   path = 'static/img/' + name + '.jpg'
      #  f.save('static/img/' + name +'.jpg')

       # with sqlite3.connect('db/database.db') as con:
        #    con.execute("INSERT INTO courses VALUES (?,?,?,?)", (name, desc, cat, path))
    
       # return redirect('/findcourse')

    #return render_template('postcourse.html')

#@app.route('/courses', methods=["GET"])
#def courses():
 #   con = sqlite3.connect('db/database.db')
  #  con.row_factory = sqlite3.Row

   # cur = con.cursor()

    #catagory = "Offshore"

    #cur.execute("SELECT * FROM courses WHERE catagory = ?",[catagory])

    #courses = cur.fetchall()

   # return render_template('courses.html', courses = courses)

#   LOGGING IN CUSTOMERS

#@app.route('/coursesavailable', methods=["GET"])
#def coursesavailable():
 #   con = sqlite3.connect('db/database.db')
  #  con.row_factory = sqlite3.Row

   # cur = con.cursor()

    #cur.execute("SELECT * FROM courses")
    #courses = cur.fetchall()

    #return render_template('coursesavailable.html', courses = courses)


#@app.route('/registercust', methods = ["GET","POST"])
#def register():
 #   if request.method == "POST":
  #      with sqlite3.connect("db/database.db") as con:
   #         email = request.form['email']
     #       username = request.form['username']
    #        password = request.form['password']

      #      passwd = password.encode('utf-8')
       #     hashedpw = bcrypt.hashpw(passwd, bcrypt.gensalt())

        #    con.execute("INSERT INTO customers VALUES(?,?,?)", (email, username, hashedpw))

         #   status = session['logged_in'] = True
          #  session['user'] = request.form['username']

           # return redirect('/')

   # return render_template("register.html")

#@app.route('/logincust', methods = ["GET","POST"])
#def login():
 #   if request.method == "POST":

  #      username = request.form['username']
 #       password = request.form['password']

  #      encodedpw = password.encode('utf-8')

    #    with sqlite3.connect("db/database.db") as con:
      #      cur = con.cursor()
        #    cur = con.execute("SELECT * FROM customers WHERE username = ?", [username])

         #   user = cur.fetchone()

          #  if cur != "":
           #     passwd = user[1]

            #    if(bcrypt.checkpw(encodedpw, passwd)):
             #       status = session['logged_in'] = True
              #      session['user'] = request.form['username']
               #     return redirect('/')
   # return render_template("login.html")

#   LOGGING IN businesses
#@app.route('/registerbus', methods = ["GET","POST"])
#def registerbus():
 #   if request.method == "POST":
  #      email = request.form['email']
   #     username = request.form['username']
    #    password = request.form['password']
     #   industry = request.form['industry']

      #  passwd = password.encode('utf-8')

       # hashpw = bcrypt.hashpw(passwd, bcrypt.gensalt())

        #with sqlite3.connect("db/database.db") as con:
         #   con.execute("INSERT INTO businesses VALUES(?,?,?,?)",(email,username,hashpw,industry))

          #  busstatus = session['bus_logged_in'] = True
           # session['user'] = request.form['username']

            #return redirect('/businesstraining')

    #return render_template("registerbus.html")

#@app.route('/loginbus', methods = ["GET","POST"])
#def loginbus():
 #   if request.method == "POST":
   #     username = request.form['username']
  #      password = request.form['password']

    
#    encodedpw = password.encode('utf-8')
#
 #       with sqlite3.connect("db/database.db") as con:
  #          cur = con.cursor()
   #         cur = con.execute("SELECT * FROM businesses WHERE username = ?", [username])

    #        user = cur.fetchone()

     #       if cur != "":
      #          passwd = user[1]

       #         if(bcrypt.checkpw(encodedpw, passwd)):
         #           busstatus = session['bus_logged_in'] = True
        #            session['user'] = request.form['username']
          #          return redirect('/businesstraining')

    #return render_template('loginbus.html')

#@app.route('/findcourse', methods=["GET", "POST"])
#@requires_login
#def findcourse():
 #   con = sqlite3.connect('db/database.db')
  #  con.row_factory = sqlite3.Row

    #cur = con.cursor()
   # catagory = "Offshore"

    #cur.execute("SELECT * FROM courses WHERE catagory = ?",[catagory])
    #course = cur.fetchall()

    #return render_template('findcourse.html', course = course)

# #Ross's stuff, can remove later
# @app.route('/findcourse', methods=["GET", "POST"])
# def findcourse():
#     con = sqlite3.connect('db/database.db')
#     con.row_factory = sqlite3.Row
    
#     cur = con.cursor()
#     catagory = "Offshore"

#@app.route('/removecourse/<id>', methods=["GET", "POST"])
#def removecourse(id):
 #   if request.method == "POST":
  #      with sqlite3.connect('db/database.db') as con:
   #         con.execute("DELETE FROM courses WHERE id = ?", [id])
    #        con.commit()

     #   return redirect('/courses')

# Creating an alternative bookcourse method

#@app.route('/bookcourse/<coursename>', methods=["POST","GET"])
#def bookcourse(coursename):
 #   if request.method == "POST":
  #      con = sqlite3.connect('db/database.db')
   #     cur = con.cursor()

    #    course = coursename
     #   user = session['user']

      #  cur.execute("SELECT * FROM customers WHERE username = ?",[user])

       # cust_data = cur.fetchone()

        #email = cust_data[0]

        #with sqlite3.connect('db/database.db') as con:
         #   con.execute("INSERT INTO bookings VALUES (?,?,?)",(course,user,email))
          #  con.commit()

   # flash("You're Successfully booked onto %s!" % course)

   # return redirect('/findcourse')


#@app.route('/peoplebooked/<coursename>', methods=["GET"])
#def peoplebooked(coursename):
 #   con = sqlite3.connect('db/database.db')
  #  cur = con.cursor()

   # cur.execute("SELECT person_booked FROM bookings WHERE course_name = ?", [coursename])

    #people = cur.fetchall()

    #return render_template('peoplebooked.html', people = people)



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
# @app.route('/findcourse', methods=["GET", "POST"])
# def findcourse():
#     con = sqlite3.connect('db/database.db')
#     cur = con.cursor()

#     cur.execute("SELECT * FROM courses WHERE catagory = ?",[catagory])
#     course = cur.fetchall()

#     return render_template('findcourse.html', course = course)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
