from flask import Flask
from flask import request, redirect, url_for
from flask import Response
from subprocess import call
import datetime 
import os
from flask import g, session, abort, render_template, flash
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods = ['GET', 'POST'])
def homepage():
    return redirect('/add_id', code=302)

@app.route("/goto_scan", methods=["POST"])
def goto_scan():
    #ids_file = open("ids.txt", "w")
    #ids_file.close()
    content = ''
    return render_template("scanner.html", content=content)

@app.route("/add_id", methods=["GET", "POST"])
def add_id():
    submission = str(request.form.get("id"))
    ids_file = open("ids.txt", 'a')
    ids_file.write(submission)
    ids_file.write('\n')
    ids_file.close()  
    try:
        with open("ids.txt", "r") as f:
            content = f.read()
    except IOError:
        # if there is no ids.txt, create an empty ids.txt
        ids_file = open("ids.txt", "w")
        ids_file.close()
        content = 'no submissions yet!'
    return render_template("scanner.html", content=content)

@app.route("/show_ids", methods = ["GET"])
def show_ids():
    try:
        with open("ids.txt", "r") as f:
            content = f.read()
    except IOError:
        # if there is no ids.txt, create an empty ids.txt
        ids_file = open("ids.txt", "w")
        ids_file.close()
        content = ''
    return render_template("submissions.html", content=content)

@app.route("/save", methods = ["POST"])
def save():
    try:
        db = sqlite3.connect('submissions.sqlite3')
    except Error as e:
        print(e)

    c = db.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS attendances''')
    new_entries = str(request.form.get("save"))
     

    return redirect('/', code=302)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80) 


