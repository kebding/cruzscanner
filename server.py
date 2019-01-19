from flask import Flask
from flask import request, redirect, url_for
from flask import Response
from subprocess import call
import datetime 
import os
from flask import g, session, abort, render_template, flash

###################SERVER_ADDR = "http://35.197.98.244"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods = ['GET', 'POST'])
def homepage():
    return url_for('static', filename='index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80) 


