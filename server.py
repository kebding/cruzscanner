from flask import Flask
from flask import request, redirect
from flask import Response
from flask import render_template
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)


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


