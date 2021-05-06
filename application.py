import os
import time

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import requests
import urllib.parse
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#  Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///speedtyping.db")


# NOT LOGGED IN

# Index
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:

        # Ensure a first name was submitted
        if not request.form.get("first"):
            return apology("Must provide a first name", 403)
        elif not request.form.get("last"):
            return apology("Must provide a last name", 403)
        elif not request.form.get("email"):
            return apology("Must provide an email address", 403)
        elif not request.form.get("password"):
            return apology("Must provide a password", 403)
        elif not request.form.get("confirmation"):
            return apology("Must confirm your password", 403)
        
        first = request.form.get("first")
        last = request.form.get("last")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            return apology("Passwords don't match", 403)

        # Query the databse for the accounts with that email
        emails_in_database = db.execute("SELECT email FROM users WHERE email = :email",
                          email=email)

        # Ensure username doesn't exist
        if len(emails_in_database) != 0:
            return apology("There is already an account with this email address", 403)
        else:
            db.execute("INSERT INTO users (firstname, lastname, email, hash) VALUES (:first, :last, :email, :hash)", first=first, last=last,
                        email=email, hash=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

        # Query database for username
        account = db.execute("SELECT * FROM users WHERE email = :email",
                          email=email)

        # Remember which user has logged in
        session["user_id"] = account[0]["id"]

        # Redirect user to home page
        return redirect("/dashboard")

# 1 Minute test
@app.route("/test1min", methods=["GET", "POST"])
def test1min():
    testLength = 1
    if request.method == "GET":
        return render_template("test.html", testLength=testLength)
    else:
        wpm = request.form.get("wpm")
        return render_template("result.html", wpm=wpm)
        db.execute("INSERT INTO tests (id, speed, date) VALUES (:id, :speed, :date)", id=session["user_id"], speed=wpm, date=time.strftime('%Y-%m-%d %H:%M:%S'))
        

# 3 Minute test
@app.route("/test3min", methods=["GET", "POST"])
def test2min():
    testLength = 3
    if request.method == "GET":
        return render_template("test.html", testLength=testLength)
    else:
        wpm = request.form.get("wpm")
        return render_template("result.html", wpm=wpm)
        db.execute("INSERT INTO tests (id, speed, date) VALUES (:id, :speed, :date)", id=session["user_id"], speed=wpm, date=time.strftime('%Y-%m-%d %H:%M:%S'))

# 5 Minute test
@app.route("/test5min", methods=["GET", "POST"])
def test3min():
    testLength = 5
    if request.method == "GET":
        return render_template("test.html", testLength=testLength)
    else:
        wpm = request.form.get("wpm")
        return render_template("result.html", wpm=wpm)
        db.execute("INSERT INTO tests (id, speed, date) VALUES (:id, :speed, :date)", id=session["user_id"], speed=wpm, date=time.strftime('%Y-%m-%d %H:%M:%S'))


# Dashboard
@app.route("/dashboard")
def dashboard():
    tests = db.execute("SELECT * FROM tests WHERE id = :id",
                          id=session["user_id"])
    return render_template("dashboard.html", tests=tests)


# LOGGED IN

# @app.route("/test")
# def test():

@app.route("/test1minLI")
@login_required
def test1minLI():
    testLength = 1
    if request.method == "GET":
        return render_template("logged_in_test.html", testLength=testLength)
    else:
        wpm = request.form.get("wpm")
        return render_template("result.html", wpm=wpm)
        db.execute("INSERT INTO tests (id, speed, date) VALUES (:id, :speed, :date)", id=session["user_id"], speed=wpm, date=time.strftime('%Y-%m-%d %H:%M:%S'))

@app.route("/tetest2minLIst3min")
@login_required
def test2minLI():
    testLength = 3
    if request.method == "GET":
        return render_template("logged_in_test.html", testLength=testLength)
    else:
        wpm = request.form.get("wpm")
        return render_template("result.html", wpm=wpm)
        db.execute("INSERT INTO tests (id, speed, date) VALUES (:id, :speed, :date)", id=session["user_id"], speed=wpm, date=time.strftime('%Y-%m-%d %H:%M:%S'))

@app.route("/test3minLI")
@login_required
def test3minLI():
    testLength = 5
    if request.method == "GET":
        return render_template("logged_in_test.html", testLength=testLength)
    else:
        wpm = request.form.get("wpm")
        return render_template("result.html", wpm=wpm)
        db.execute("INSERT INTO tests (id, speed, date) VALUES (:id, :speed, :date)", id=session["user_id"], speed=wpm, date=time.strftime('%Y-%m-%d %H:%M:%S'))


# Log in
@app.route("/login", methods=["GET", "POST"])
@login_required
def login():

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for email
        emails_in_database = db.execute("SELECT * FROM users WHERE LOWER(email) == LOWER(:email)",
                          username=request.form.get("email"))


        # Ensure username exists and password is correct
        if len(emails_in_database) != 1 or not check_password_hash(emails_in_database[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = emails_in_database[0]["id"]

        # Redirect user to home page
        return redirect("/dashboard")


@app.route("/logout")
@login_required
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to index
    return redirect("/")






# CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'firstname' TEXT NOT NULL, 'lastname' TEXT NOT NULL, 'email' TEXT NOT NULL);
# CREATE TABLE IF NOT EXISTS "tests" ('id' INTEGER, 'speed' INTEGER, 'date' DATETIME);