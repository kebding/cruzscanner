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
    return app.send_static_file('index.html')

@app.route("/scanner", methods=["GET", "POST"])
def scanner():
    if request.method == "POST":
        content = get_current_settings()
    else:
        content = 'no submissions yet'
        # clear ids.txt
        ids_file = open("ids.txt", "w")
        ids_file.close()
    section = get_section()
    week = get_week()
    return render_template("scanner.html", content=content, 
            current_section=section, current_week=week)

@app.route("/save", methods = ["POST"])
def save():
    try:
        db = sqlite3.connect('submissions.sqlite3')
    except Error as e:
        print(e)

    c = db.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS attendances''')
    section_and_week= str(request.form.get("save_to_db"))
     

    return redirect('/', code=302)
    


def get_section():
    try:
        with open("section.txt", "r") as f:
            section = f.read().rstrip()
        f.close()
    except IOError:
        section_file = open("section.txt", "w")
        section_file.write("01A")
        section_file.close()
        section = "01A"
    return section

def get_week():
    try:
        with open("week.txt", "r") as f:
            week = f.read().rstrip()
        f.close()
    except IOError:
        week_file = open("week.txt", "w")
        week_file.write("1")
        week_file.close()
        week = "1"
    return week

def get_current_settings():
    #TODO: replace ids.txt with database 
    submission = str(request.form.get("id_entry"))
    if submission is not None and submission != "None":
        ids_file = open("ids.txt", 'a')
        ids_file.write(submission)
        ids_file.write('\n')
        ids_file.close()  
    try:
        with open("ids.txt", "r") as f:
            content = f.read()
        f.close()
    except IOError:
        # if there is no ids.txt, create an empty ids.txt
        ids_file = open("ids.txt", "w")
        ids_file.close()
        content = 'no submissions yet'
    week = str(request.form.get("week"))
    if week is not None and week != "None":
        week_file = open("week.txt", "w")
        week_file.write(week)
        week_file.close()
    section = str(request.form.get("section"))
    if section is not None and section != "None":
        section_file = open("section.txt", "w")
        section_file.write(section)
        section_file.close()

    return content

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80) 


