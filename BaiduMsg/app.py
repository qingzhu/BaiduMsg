#!/usr/bin/env python
#coding: utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import os
import StringIO, gzip
import re
import json

import TiebaMsg
from baidu import Verify
from DB import DB

class SendMsgHandler(object):
    def __init__(self, username, password):
        self.gif_path = None
        self.verifyStr = None
        self.code = None

        self.username = username
        self.password = password
        
        TiebaMsg.login(username, password)

    def init(self):
        self.verifyStr = TiebaMsg.get_verify()
        gif_time = TiebaMsg.get_gif(self.verifyStr)
        self.gif_path  = 'static/%s.gif' % gif_time

        #print 'verifyStr:%s' % self.verifyStr
        #print 'gif_path:%s' % self.gif_path

        self.vcode()
        #print 'code:%s' % self.code
    
    def vcode(self):
        global mycode
        
        result = mycode.get(self.gif_path)
        self.code = result


    def logout(self):
        TiebaMsg.logout()

    def send(self, unames):
        while True:
            self.init()
            print self.code,len(self.code)
            if len(self.code) == 4:
                break

        with open('content.txt','r') as f:
            content = f.read()

        try:
            token = TiebaMsg.get_bdstoken()
            print 'token:%s' % token
            result    = TiebaMsg.sendMessage(unames, content, self.verifyStr, self.code, token)
            #print 'result:%s' % result 
            try:
                gf = gzip.GzipFile(fileobj=StringIO.StringIO(result),mode='r')
                html = gf.read()
            except:
                gf = gzip.GzipFile(fileobj=StringIO.StringIO(result),mode='r')
                html = gf.extrabuf
            finally:
                if 'errorNo : "0"' in html:
                    return 1
                else:
                    print html.decode('utf-8','ignore').encode('gb2312','ignore')
                    return 0
        except Exception,e:
            TiebaMsg.login(self.username, self.password)
          
        

def main():
    db = DB('myun.db')

    with open('last_num.txt') as f:
        num = int(f.read())

    account = 'kyshipin%03d@kyshipin.com' % (num/100+1)
    #account = 'kyshipin002@kyshipin.com'
    print 'Start from num:%s, use:%s' % (num, account)
    while True:
        if num % 100 == 0:
            xiaohao.logout()
            account = 'kyshipin%3d@kyshipin.com' % (num/100+1)

        xiaohao = SendMsgHandler(account, 'woshixiaohao')
        
        unames = db.get_uns(num)
        print 'unames:%s' % unames.decode('utf-8','ignore').encode('gb2312','ignore')
        while True:
            result = xiaohao.send(unames)
            if result:
                print 'Successful:%s,%s' % (num, unames.decode('utf-8','ignore').encode('gb2312','ignore'))
                break
        with open('last_num.txt','w') as f:
            f.write(str(num))
        num += 5

            
mycode = Verify()


if __name__ == "__main__":
    main()
