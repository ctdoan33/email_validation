from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
app = Flask(__name__)
app.secret_key = "KeepItSecretKeepItSafe"
mysql = MySQLConnector(app,"email_db")
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/validate", methods=["POST"])
def validate():
    if len(request.form["email"]) < 1:
        flash("Email must not be blank!")
    elif not EMAIL_REGEX.match(request.form["email"]):
        flash("Email is not valid!")
    else:
        session["newemail"] = request.form["email"]
        query = "INSERT INTO emails (email_address, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
            "email" : request.form["email"]
        }
        mysql.query_db(query, data)
        return redirect("/success")
    return redirect("/")
@app.route("/success")
def success():
    query = "SELECT email_address, DATE_FORMAT(created_at, '%m/%d/%y %I:%i %p') AS date FROM emails"
    emails = mysql.query_db(query)
    return render_template("success.html", all_emails=emails)
app.run(debug=True)
