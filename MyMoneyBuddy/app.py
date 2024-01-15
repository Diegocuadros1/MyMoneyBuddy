import os

from flask import Flask, render_template, flash, redirect, request, session
from flask_session import Session
import hashlib
import sqlite3
from helpers import usd, login_required, apology

#configuring application
app = Flask(__name__)

#custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Configure SQL to use database
sql = sqlite3.connect('data.db')
db = sql.cursor()

#after request
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    '''bar graph'''
    with db.connection("data.db"):
      return render_template("Hello World!")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    '''Logging User in'''
    with db.connection('data.db'):
        if request.method == "POST":
            #ensure username was submitted
            if not request.form.get("username"):
                return apology("must provide username", 400)

            # Ensure password was submitted
            elif not request.form.get("password"):
              return apology("must provide password", 400)

            return render_template("loggin in")
        else:
            return render_template("login")

@app.route("/logout")
def logout():
    
    #forget user info
    session.clear()

    #redirecting user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """registering user"""
    
    with db.connection('data.db'): 
      if request.method == "POST":
          '''register user'''
          return render_template("registration page")

      else:
          '''method = POST'''
          return render_template("register.html")
