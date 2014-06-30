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
from sixin.baidu import Verify

class SendMsgHandler(object):
    def __init__(self, username, password):
        self.gif_path = None
        self.verifyStr = None
        self.code = None
        
        TiebaMsg.login(username, password)

    def init(self):
        self.verifyStr = TiebaMsg.get_verify()
        gif_time = TiebaMsg.get_gif(self.verifyStr)
        self.gif_path  = 'static/%s.gif' % gif_time

        self.vcode()
    
    def vcode(self):
        global vcode
        while True:
            result = vcode.get(self.gif_path)
            if len(result) == 4:
                self.code = result
                break

    def logout(self):
        TiebaMsg.logout()

    def send(self, unames):
        self.init()

        with open('content.txt','r') as f:
            content = f.read()

        try:
            token = TiebaMsg.get_bdstoken()
            result    = TiebaMsg.sendMessage(unames, content, self.verifyStr, self.code, token)
        except Exception,e:
            print e

        try:
            gf = gzip.GzipFile(fileobj=StringIO.StringIO(result),mode='r')
            html = gf.read()
        except:
            gf = gzip.GzipFile(fileobj=StringIO.StringIO(result),mode='r')
            html = gf.extrabuf
        
        if 'errorNo : "0"' in html:
            return 1
        else:
            print html
            return 0
            
vcode = Verify()

if __name__ == "__main__":
    xiaohao = SendMsgHandler('kyshipin001@163.com', 'woshixiaohao')
    unames = 'KY视频001;KY视频002;KY视频003;KY视频004;KY视频005;'
    while True:
        result = xiaohao.send(unames)
        if result:
            break
    
    xiaohao.logout()
    print 'Send Successful!'
