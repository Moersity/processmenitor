#!/bin/env python
# -*- coding: utf-8 -*-
# @Filename: dbhelper
# @Author: bigman
# @Date: 2018/1/11
import sqlite3
import logging
import time

import psutil
import sys

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
d = {'clientip': 'localhost', 'user': 'dbhelper'}
logger = logging.getLogger('dbhelper')

logger.setLevel('INFO')
conn = sqlite3.connect('processinfo.db')
logger.info("Database connection established ",extra=d)

def initialTable():
    c = conn.cursor()
    sql = '''
     CREATE TABLE PROCESS
    (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
     PID  INT                NOT NULL,
     TIME DOUBLE          NOT NULL,
     CPUPERCENT FLOAT    NOT NULL

      );
    '''

    try:
        c.execute("DROP TABLE process")
        c.execute(sql)
        conn.commit()
    except sqlite3.OperationalError:
        return
def updateData():
    c = conn.cursor()
    id = 0
    while True:

        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
            except:
                pass
            percent = p.cpu_percent(0.1)
            para = (id,pid,time.time(),percent)
            id += 1
            sql = "insert into process VALUES (?,?,?,?)"
            c.execute(sql,para)
            conn.commit()


if __name__ == '__main__':
    c = conn.cursor()
    pid = (4,)
    c.execute("select time,cpupercent from process where pid = ?", pid)
    for res in c.fetchall():
        print(res)
    conn.close()





