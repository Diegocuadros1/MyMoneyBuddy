import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", error=code, placeholder=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def sql_to_list(info):

    list_of_stuff = []
    extra_dict = {}
    new_list = []

    for item in info:
        list_of_stuff.append([item["category"], item["price"]])

    #print(list_of_stuff)

    for item in list_of_stuff:
        if item[0] not in extra_dict:
            extra_dict[item[0]] = item[1]
        else:
            extra_dict[item[0]] += item[1]

    for key, value in extra_dict.items():
        new_list.append([key, value, "red"])

    return new_list

def turn_to_percent(sql_list):
    total = 0
    for item in sql_list:
        total += item[1]

    for item in sql_list:
        item[1] = round((item[1] / total) * 100)

    return sql_list

def find_most_spent(my_list):
    total = 0
    for item in my_list:
        if item[1] > total:
            total = item[1]
            category = item[0]

    return category, total
