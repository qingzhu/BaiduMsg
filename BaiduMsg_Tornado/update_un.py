#!/usr/bin/env python
#coding: utf8
import urllib
import urllib2
import re

first = None
def get_uname(pageurl, urltype):
    global first
    if urltype == 2:
        f = open(pageurl,'r')
        html = f.read()
        f.close()
    else:
        html = urllib2.urlopen(pageurl).read()
    p = re.compile(r'(?<=href="/home/main\?un=).*?(?=")')
    uns = p.findall(html)

    if urltype == 0 or urltype == 2:
        uns = [x for i,x in enumerate(uns) if i%2]
        if len(uns) > 0:
            first = uns[0]
    else:
        duishou = []
        bawu = []
        uns = list(set(uns) - set(duishou) - set(bawu))

    for un in uns:
        uname = urllib.unquote(un).decode('gbk', 'ignore').encode('utf-8', 'ignore')
        yield uname

def get_page(url, save_name):
    html = urllib2.urlopen(url).read()
    with open(save_name, 'w') as f:
        f.write(html)
    print '%s has get!' % save_name

def exist_un(name, i):
    with open('data.txt','r') as f:
        for line in f:
            if name == line.strip('\n'):
                #print name,'has exist in page',i+1
                return 1
    return 0

def quchong(filename):
    new = []
    with open(filename,'r') as f:
        for line in f:
            if line in new:
                print line.strip('\n')
                continue
            new.append(line)
    if len(new) > 0:
        with open(filename,'w') as f:
            f.writelines(new)

def update_un(pn):
    new = []
    after = []
    for i in xrange(pn):
        names = get_uname('http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=%BF%BC%D1%D0&pn='+str(i+1), 0)
        for name in names:
            if exist_un(name, i):
                if len(new)>0:
                    with open('data.txt','r+') as f:
                        after = new + f.readlines()
                    with open('data.txt','w') as f:
                        f.writelines(after)
                        print '已经将新的un更新到记录文件！'
                        return 1
                else:
                    #print '未检测到新的un。'
                    return 0
            new.append(name+'\n')
            print '有新的un：',name
        print "page %s has finished!" % str(i+1)
    
def get_new_un(num):
    import time

    while True:
        update_un(num)
        time.sleep(3)

if __name__ == "__main__":
    get_new_un(1000)

