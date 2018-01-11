import psutil
import json
from dbhelper import conn
class pModel:
    def __init__(self,pid):
        self.cpu_percent,self.memory_percent= [],[]
        cur = conn.cursor()
        cur.execute('select * from process where pid=? order BY CPUPERCENT DESC ',(pid,))
        for line in cur.fetchall():
            info = json.loads(line[5])
            self.cpu_percent.append((line[3],line[4]))
            self.memory_percent.append((line[3],info['memory_percent']))
            self.name = line[2]
            self.pid = line[1]
            self.info = line[5]
        cur.close()

    def tojson(self):
        attrs = [d for d in dir(self) if str(d)[:2] != '__' and str(d)!='tojson']
        res = {}
        for a in attrs:
            res[a] = self.__getattribute__(a)
        res["info"] = res["info"].replace("\\","")
        return json.dumps(res)

