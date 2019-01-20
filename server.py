from flask import Flask
from flask import request, redirect
from flask import Response
from flask import render_template
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

@app.route("/scanner", methods=["GET", "POST"])
def scanner():
    if request.method == "POST":
        submit_attendance(request)
        attendances,section,week = get_current_settings(request)
    else:
        attendances = 'no attendances yet'
        # go with default week and section
        section = "01A"
        week = "1"
    return render_template("scanner.html", attendances=attendances,
            current_section=section, current_week=week)

@app.route("/exams", methods=["GET"])
def exams():
    content = ''
    return render_template("exams.html", content=content)

@app.route("/upload", methods=["POST"])
def upload():
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    df = pandas.read_csv('db/db.csv')
    df.to_sql('roster', con, if_exists='append', index=False)
    #get_posts()
    return redirect('/', code=302)

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

def submit_attendance(request):
    try:
        db = sqlite3.connect('db/attendances.sqlite3')
    except Error as e:
        print(e)
        return

    c = db.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS attendances(
        id TEXT,
        section TEXT,
        week TEXT
        )''')

    sid = str(request.form.get("id_entry"))
    section = str(request.form.get("section"))
    week = str(request.form.get("week"))

    c.execute("INSERT INTO attendances VALUES (?,?,?)", (sid,section,week))

    db.commit()
    db.close()

    return redirect('/', code=302)


def get_current_settings(request):
    section = str(request.form.get("section"))
    week = str(request.form.get("week"))
    try:
        db = sqlite3.connect('db/attendances.sqlite3')
    except Error as e:
        print(e)
        return
    c = db.cursor()
    c.execute("SELECT DISTINCT id FROM attendances WHERE section=? AND week=?",
        (section, week))
    attendances_raw = c.fetchall()
    db.close()

    attendances = ''
    for i in attendances_raw:
        attendances = attendances + str(i[0]) + '\n'

    return attendances,section,week

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80) 


