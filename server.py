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
        #update_db()
        submissions,section,week = get_current_settings(request)
    else:
        submissions = 'no submissions yet'
        # clear ids.txt
        ids_file = open("ids.txt", "w")
        ids_file.close()
        # go with default week and section
        section = "01A"
        week = "1"
    return render_template("scanner.html", submissions=submissions,
            current_section=section, current_week=week)

def update_db(request):
    try:
        db = sqlite3.connect('submissions.sqlite3')
    except Error as e:
        print(e)
        return

    c = db.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS attendances''')
    
    sid = str(request.form.get("id_entry"))
    section = str(request.form.get("section"))
    week = str(request.form.get("week"))

    c.execute("INSERT INTO attendances VALUES ({},{},{})" % sid, section, week)

    return redirect('/', code=302)


def get_current_settings(request):
    #TODO: replace ids.txt with database 
    submission = str(request.form.get("id_entry"))
    if submission is not None and submission != "None":
        ids_file = open("ids.txt", 'a')
        ids_file.write(submission)
        ids_file.write('\n')
        ids_file.close()  
    try:
        with open("ids.txt", "r") as f:
            submissions = f.read()
        f.close()
    except IOError:
        # if there is no ids.txt, create an empty ids.txt
        ids_file = open("ids.txt", "w")
        ids_file.close()
        submissions = 'no submissions yet'
    section = str(request.form.get("section"))
    week = str(request.form.get("week"))

    return submissions,section,week

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80) 


