#!/bin/env python
# -*- coding: utf-8 -*-
# @Filename: dbhelper
# @Author: bigman
# @Date: 2018/1/11
import json
import sqlite3
import logging
import time

import psutil
import sys

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
d = {'clientip': 'localhost', 'user': 'dbhelper:'}
logger = logging.getLogger('dbhelper')

logger.setLevel('INFO')
conn = sqlite3.connect('processinfo.db')
logger.info("Database connection established ", extra=d)


def initialTable():
    c = conn.cursor()
    sql = '''
     CREATE TABLE PROCESS
    (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
     PID                  NOT NULL,
     PNAME VARCHAR        NOT NULL,
     TIME int          NOT NULL,
     CPUPERCENT FLOAT     NOT NULL,
     INFO VARCHAR         NOT NULL,
     CREATE_TIME INT       NOT NULL

      );
    '''

    try:
        c.execute("DROP TABLE process")
    except Exception as e:
        print(e)

    c.execute(sql)
    conn.commit()
    c.close()
    logger.info("table process created",extra=d)



def updateData():

    while True:
        c = conn.cursor()
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
            except:
                continue
            percent = p.cpu_percent(0.1)
            info = json.dumps(dict(p.as_dict()))
            paper = dict(p.as_dict())
            create_time = paper["create_time"]
            para = (pid,p.name(), int(time.time()), percent,info,create_time)
            sql = "insert into process (pid,pname,time,cpupercent,info,create_time) VALUES (?,?,?,?,?,?)"
            c.execute(sql, para)
            conn.commit()
            #print(create_time)
            logger.info("inset process "+str(pid)+"information to process table",extra=d)
        c.close()


if __name__ == '__main__':
 #  initialTable()
    updateData()

