import sqlite3
from flask import Flask
import psutil
import json
import time
from processmodel import pModel
from flask import render_template
from dbhelper import conn

app = Flask(__name__)
@app.route('/')
def index():
    pids = psutil.pids()
    try:
        process_infos = [pModel(pid) for pid in pids]
        for p in process_infos:
            if hasattr(p,'info'):
                p.info = json.loads(p.info)
                p.create_time = time.strftime( "%Y-%m-%d %H:%M:%S",time.localtime(p.create_time))
                p.hasinfo = True
            else:
                p.hasinfo = False

        return render_template('index.html',process_info=process_infos)
    except Exception as e:
        print(e.with_traceback())
        return "ok"
@app.route('/detail/<string:pid>')
def detail(pid):
    return render_template('detail.html',pid=pid)

@app.route('/process/<int:pid>')
def process_info(pid):

    return pModel(pid).tojson()



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
