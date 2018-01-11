import sqlite3
from flask import Flask
import psutil
import json
import time
from processmodel import pModel
from flask import render_template

app = Flask(__name__)
@app.route('/')
def index():
    pids = psutil.pids()
    try:
        names = [psutil.Process(p).name() for p in pids if psutil.Process(p)]
        process = zip(pids,names)
        return render_template('index.html', process = process)
    except:
        return "ok"
@app.route('/detail/<string:pid>')
def detail(pid):
    return render_template('detail.html',pid=pid)

@app.route('/process/<int:pid>')
def process_info(pid):

    return pModel(pid).tojson()



if __name__ == '__main__':
    app.run()
