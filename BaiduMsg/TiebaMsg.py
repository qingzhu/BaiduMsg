#!/usr/bin/env python
# -*- coding: utf8 -*-
import urllib2
import urllib
import cookielib
import re
import time

def login(name, passwd):
    URL_BAIDU_INDEX = u'http://www.baidu.com/';
    #https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true 也可以用这个
    URL_BAIDU_TOKEN = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login';
    URL_BAIDU_LOGIN = 'https://passport.baidu.com/v2/api/?login';
  
    #设置用户名、密码
    username = name;
    password = passwd;
  
    #设置cookie，这里cookiejar可自动管理，无需手动指定
    cj = cookielib.CookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
    urllib2.install_opener(opener);
    reqReturn = urllib2.urlopen(URL_BAIDU_INDEX);
  
    #获取token
    tokenReturn = urllib2.urlopen(URL_BAIDU_TOKEN);
    matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"',tokenReturn.read());
    tokenVal = matchVal.group('tokenVal');
    
    codestring = login_check(tokenVal,name)
    if codestring:
        verifycode = get_verifycode(codestring)
    else:
        verifycode = ''
  
    #构造登录请求参数，该请求数据是通过抓包获得，对应https://passport.baidu.com/v2/api/?login请求
    postData = {
        'username' : username,
        'password' : password,
        'u' : 'https://passport.baidu.com/',
        'tpl' : 'pp',
        'token' : tokenVal,
        'codestring': codestring,
        'verifycode': verifycode,
        'staticpage' : 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
        'isPhone' : 'false',
        'charset' : 'UTF-8',
        'callback' : 'parent.bd__pcbs__ra48vi'
        };
    postData = urllib.urlencode(postData);
  
    #发送登录请求
    loginRequest = urllib2.Request(URL_BAIDU_LOGIN,postData);
    loginRequest.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
    loginRequest.add_header('Accept-Encoding','gzip,deflate,sdch');
    loginRequest.add_header('Accept-Language','zh-CN,zh;q=0.8');
    loginRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
    loginRequest.add_header('Content-Type','application/x-www-form-urlencoded');
    sendPost = urllib2.urlopen(loginRequest);

def login_check(token,name):
    url = 'https://passport.baidu.com/v2/api/?logincheck&token=%s&tpl=pp&apiver=v3&tt=%s&username=%s&isphone=false&callback=bd__cbs__mjp2jp' % (token, int(time.time()), name)
    
    result = urllib2.urlopen(url).read()
    match = re.search(u'"codeString" : "(?P<codestring>.*?)"', result)
    codestring = match.group('codestring')
    print 'codestring:%s' % codestring
    return codestring

def get_verifycode(codestring):
    url = 'https://passport.baiducom/cgi-bin/genimage?%s' % codestring
    print 'verifycode_url:%s' % url
    gif = urllib2.urlopen(url).read()
    with open('login_verify.gif','wb') as f:
        f.write(gif)

    while True:
        code = raw_input('请输入验证码，login_verify.gif：'.decode('utf-8','ignore').encode('gb2312','ignore'))
        if len(code.rstrip())== 4:
            break
    return code

def get_verify():
    verify_url = "https://passport.baidu.com/v2/?reggetcodestr&tpl=qing&app=stelyg&apiver=v3&class=reg&echoback=msg.home.editor.changeVerifyCode&tt=%s&callback=msg.msgpublish.Form.changeVerifyCode" % int(time.time())
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
        'Host':'passport.baidu.com',
        'Accept':'*/*',
        'Referer':'http://msg.baidu.com/msg/writing',
        'Connection':'keep-alive'
    }
    req = urllib2.Request(
        url = verify_url,
        headers = headers
    )

    result = urllib2.urlopen(req).read()
    p = re.compile(r'(?<="verifyStr" : ").*?(?=")')
    verify = p.findall(result)[0]
    return verify

def get_gif(verify):
    gif_time = int(time.time())
    gif_url = 'https://passport.baidu.com/cgi-bin/genimage?%s&t=%s' % (verify,gif_time)

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
        'Host':'passport.baidu.com',
        'Accept':'image/png,image/*;q=0.8,*/*;q=0.5',
        'Referer':'http://msg.baidu.com/msg/writing',
        'Connection':'keep-alive'
    }
    gif = urllib2.urlopen(gif_url).read()
    with open('static/%s.gif' % gif_time,'wb') as f:
        f.write(gif)
    return gif_time

def get_bdstoken():
    bdstoken_url = 'http://msg.baidu.com/?t=%s' % int(time.time())
    
    headers = {
        'Host':'msg.baidu.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer':'http://msg.baidu.com/msg/writing',
        'Connection':'keep-alive'
    }

    req = urllib2.Request(
        url = bdstoken_url,
        headers = headers
    )

    result = urllib2.urlopen(req).read()
    p = re.compile(r'(?<=msgBdsToken = ").*?(?=";)')
    with open('bdstoken.html','w') as f:
        f.write(result)

    bdstoken = p.findall(result)[0]
    return bdstoken

def sendMessage(un, content, verify, code, token):
    # 1.获取erifyStr
    #verifyStr = get_verify()
    verifyStr  = verify

    # 2.获取验证码图片
    #gif_time = get_gif(verifyStr)

    # 3.读取验证码
    #vcode = raw_input('qing shuru yangzhengma: %s.gif' % gif_time).rstrip('\n')
    vcode = code

    # 4.获取bdstoken
    #bdstoken = get_bdstoken(un)
    bdstoken = token

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer':'http://msg.baidu.com/msg/writing',
        'Connection':'keep-alive',
        'Host':'msg.baidu.com'
    }
    
    post_url = 'http://msg.baidu.com/msg/writing/submit/msg'
    post_data = {
        'msgcontent': content,
        'vcode': vcode,
        'msgvcode': verifyStr,
        'msgreceiver': un,
        'bdstoken': bdstoken,
        'qing_request_source':''
    }
    post_data = urllib.urlencode(post_data)
    req = urllib2.Request(
        url = post_url,
        data = post_data,
        headers = headers
    )
    
    result = urllib2.urlopen(req).read()
    return result

def logout():
    url = 'http://passport.baidu.com/?logout&tpl=mn&u=http://www.baidu.com/'
    urllib2.urlopen(url)


if __name__ == "__main__":
    login('aini2143@163.com','13145202143')
    # 5.发送私信
    for i in xrange(6):
        print i
        verify = get_verify()
        get_gif(verify)
    raw_input('quit#')
    code = raw_input('input vcode:').rstrip('\n')
    token = get_bdstoken('noiieqe39812')
    print sendMessage('noiieqe39812', 'hello,boy', verify, code, token)
