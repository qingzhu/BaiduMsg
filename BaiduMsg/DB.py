#!/usr/bin/env python
#coding: utf8

import sqlite3
import os.path

class DB(object):
    """
        连接SQLite
    """
    def __init__(self, db):
        self.db = db
        self.init()

    def init(self):
        if os.path.exists(self.db):
            pass
        else:
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()

            cur.execute('create table user(id integer primary key,un varchar(20))')
            conn.commit()
            conn.close()

    def update_un(self, filename):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        num = 0
        with open(filename,'r') as f:
            for line in f:
                uname = line.rstrip('\n')
                if uname:
                    num += 1
                    #print uname
                    print num, uname.decode('utf-8','ignore').encode('gb2312','ignore')
                    cur.execute("insert into user values(%s,'%s')" % (num, uname))

        conn.commit()
        conn.close()

    def get_uns(self, num):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        
        start = num
        sql = 'select un from user where id>=%s and id<%s' % (start, start+5)
        query = cur.execute(sql)
        result = query.fetchall()
        
        uns = [result[i][0] for i in range(5)]
        return ';'.join(uns) + ';'

if __name__ == "__main__":
    db = DB('myun.db')
    #db.update_un('new.txt')
    print db.get_uns(1)