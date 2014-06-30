#!/usr/bin/env python
#coding: utf8

import MySQLdb


def get_un(num):
    db = MySQLdb.connect(host='localhost', user='root',passwd='tjh13145202143',db='Tieba', charset='utf8')
    cursor = db.cursor()
    start = (num-1)*5 + 1

    cursor.execute('select un from user where id>=%s and id<%s' % (start, start+5))
    result = cursor.fetchall()
    uns = [result[i][0] for i in range(5)]

    return ';'.join(uns) + ';'

def update_un(filename):
    db = MySQLdb.connect(host='localhost',user='root',passwd='tjh13145202143',db='Tieba',charset='utf8')
    cursor = db.cursor()
    num = 0
    with open(filename,'r') as f:
        for line in f:
            uname = line.rstrip('\n')
            if uname:
                num += 1
                #print uname
                cursor.execute("insert user(id,un) values(%s,'%s')" % (num, uname))
    db.commit()
    db.close()
    print "%s record has insert into the database!" % num


if __name__ == "__main__":
    update_un('test.bak')
