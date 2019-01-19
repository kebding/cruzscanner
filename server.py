from flask import Flask
from flask import request, redirect, url_for
from flask import Response
from subprocess import call
import datetime 
import os
from flask import g, session, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods = ['GET', 'POST'])
def homepage():
    return app.send_static_file('index.html')

@app.route("/add_id", methods=["POST"])
def add_id():
    if request.method != "POST":
        return "bad request"
    submission = str(request.form.get("id"))
    ids_file = open("ids.txt", 'a')
    ids_file.write(submission)
    ids_file.write('\n')
    ids_file.close()
    return redirect('/', code=302)

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


