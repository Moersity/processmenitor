import sqlite3
from flask import Flask
import psutil
import json

from flask import render_template

app = Flask(__name__)
@app.route('/')
def index():
    pids = psutil.pids()
    names = [psutil.Process(p).name() for p in pids]
    process = zip(pids,names)
    return render_template('index.html', process = process)
@app.route('/detail/<string:pid>')
def detail(pid):
    return render_template('detail.html',pid=pid)

@app.route('/process/<int:pid>')
def process_info(pid):
    conn = sqlite3.connect('processinfo.db')
    c = conn.cursor()
    pid = (4,)
    c.execute("select time,cpupercent from process where pid = ?", pid)
    for res in c.fetchall():
        print(res)
    return json.dumps('')


if __name__ == '__main__':
    app.run()
