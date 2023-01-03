from hashlib import sha256
import string
import os
import sqlite3 
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Markup
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from email.message import EmailMessage
import ssl
import smtplib

em = EmailMessage()


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = '12345'

con = sqlite3.connect("techwar.db", check_same_thread=False)
db = con.cursor()
print("Database connected")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None: 
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
@login_required
def index():
    return render_template("home.html")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    session.clear()
   
    db = con.cursor()
    if request.method == 'POST':
        name = request.form.get("name")
        password = request.form.get("password")
        for user in db.execute('select username from users'):
            user = user[0]
        for pasw in db.execute('select password from users'):
            pasw = pasw[0]
        for user_id in db.execute('select id from users'):
            user_id = user_id[0]
        if not name:
            message = "You need to write down your Username"
            return render_template("error-login.html", message=message)
        elif not password:
            message = "Without a password we cannot let you in, buddy"
            return render_template("error-login.html", message=message)
        elif name not in user:
            message = "Invalid Username"
            return render_template("error-login.html", message=message)
        if not check_password_hash(pasw, password):
            message = "Invalid password, make sure you wrote it right"
            return render_template("error-login.html", message=message)
        session["user_id"] = user_id
        return redirect("/")

    return render_template("login.html")
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        if email:
                email_sender = "josh.s.project.s.6@gmail.com"
                email_password = "pbklmrdugprjlskx"
                email_receiver = request.form.get("email")
                subject = "CS50 - Final Project"
                body = """This 'Final Project' is, I hope, the beginning of a browser game, but...I'm just starting. 
                
                Thank you!
                """        
        elif not email:
                message = "Sorry, we need an E-mail to continue"
                return render_template("error.html", message=message)

        if not username:
            message = "Sorry! You must provide a username"
            return render_template("error.html", message=message)
            
        elif not password:
            message = "Sorry! You must provide a password"
            return render_template("error.html", message=message)
        elif not request.form.get("confirm"):
            message = "Please! Confirm your password!"
            return render_template("error.html", message=message)
        elif password != request.form.get("confirm"):
            message = "The passwords do not match"
            return render_template("error.html", message=message)
        

        
        dic = {'upper':[],'lower':[], 'special character':[], 'number':[]}
        for charc in password:
            if ord(charc) in list(range(97, 123)):
                dic['lower'].append(charc)
            elif ord(charc) in list(range(65, 91)):
                dic['upper'].append(charc)
            elif ord(charc) in list(range(48, 58)):
                dic['number'].append(charc)
            else:
                dic['special character'].append(charc)


        for index, value in dic.items():
            if len(value)<1:
                message ="Password must contain at least 1 {} character".format(index)
                return render_template("error.html", message=message)
        
        for emails in db.execute("SELECT email FROM users"):
            emails = emails[0]
        for usernames in db.execute("SELECT username FROM users"):
            usernames = usernames[0]
        if email in emails:
            message = "There is already an account with that email"
            return render_template("error.html", message=message)
        elif username in usernames:
            message = "Username already used, pick another one"
            return render_template("error.html", message=message)
            

        
        hash = generate_password_hash(password, 'sha256')
        db.execute("INSERT INTO users(username, password, email) VALUES(?, ?, ?)", (username, hash, email))
        con.commit()
        flash('Account created succesfully!')
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver,em.as_string())

        return render_template("login.html")
        
    else:      
        return render_template("register.html")
        

 