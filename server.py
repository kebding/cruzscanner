from flask import Flask
from flask import request, redirect, url_for
from flask import Response
from subprocess import call
import datetime 
import os
from flask import g, session, abort, render_template, flash

import sqlite3
import pandas
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config.from_object(__name__)

    #def get_posts():
    #   with con:
    #       cur.execute("SELECT * FROM roster")
    #       print(cur.fetchall())

@app.route("/", methods = ['GET', 'POST'])
def homepage():
    return app.send_static_file('index.html')

@app.route("/goto_scan", methods=["POST"])
def goto_scan():
    ids_file = open("ids.txt", "w")
    ids_file.close()
    content = ''
    return render_template("scanner.html", content=content)

@app.route("/goto_exams", methods=["POST"])
def goto_exams():
    ids_file = open("ids.txt", "w")
    ids_file.close()
    content = ''
    return render_template("exams.html", content=content)

@app.route("/upload", methods=["POST"])
def upload():
    #ids_file = open("ids.txt", "w")
    #ids_file.close()
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    df = pandas.read_csv('db.csv')
    df.to_sql('roster', con, if_exists='append', index=False)
    #get_posts()
    return redirect('/', code=302)

@app.route("/add_id", methods=["POST"])
def add_id():
    if request.method != "POST":
        return "bad request"
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
        content = ''
    return render_template("scanner.html", content=content)

@app.route("/exam_id", methods=["POST"])
def exam_id():
    if request.method != "POST":
        return "bad request"
    submission = str(request.form.get("id"))
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    t = (submission,)
    cur.execute("SELECT email FROM roster WHERE id = ?", t)
    s1 = str(cur.fetchone())
    s2 = s1[3:]
    s3 = s2[:-3]
    ids_file = open("examids.txt", 'w')
    if len(s3) == 0:
        ids_file.write( "NOT FOUND!")
        ids_file.write('\n')
        ids_file.close()
    else:
        ids_file.write( "Student Found: "+ s3 + " has been notified")
        ids_file.write('\n')
        ids_file.close()

        fromaddr = "tas.ucsc@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = s3
        msg['Subject'] = "CMPE 16 Exam Submission Confirmation"
        body = "Hi,\n\nWe got your exam broski, you is gucci <3\n\nLove TAs"
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "CruzHacks@2019")
        text = msg.as_string()
        server.sendmail(fromaddr, s3, text)
        server.quit()

    try:
        with open("examids.txt", "r") as f:
            content = f.read()
    except IOError:
        # if there is no examids.txt, create an empty ids.txt
        ids_file = open("examids.txt", "w")
        ids_file.close()
        content = ''
    return render_template("exams.html", content=content)

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

@app.route("/clear", methods = ["POST"])
def clear_ids():
    ids_file = open("ids.txt", "w")
    ids_file.close()
    return redirect('/', code=302)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80) 


