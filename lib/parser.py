#encoding:utf-8
import optparse
import sys
def findall(body,arg,start=0):
    result = []       
    while True:
        pos = body.find(arg, start)
        if pos >= 0:
            result.append(pos)
            start = pos + len(arg)
            continue
        break
    return result

def format(data):
    s=findall(data,"&") 
    i=0     
    arg=0
    a={}
    length=len(s)
    while i < len(s):
            q=data[arg:s[i]]
            d=q.split('=')
            a[d[0]]=d[1]
            arg=arg+s[i]+1
            i=i+1
    last=data[s[length-1]+1:]
    final=last.split('=')
    a[final[0]]=final[1]
    return a

def parse():
    parser = optparse.OptionParser('usage: %prog [options] target')
    parser.add_option('-u',dest='url',help='target url')
    parser.add_option('--data',dest='data',help='post data',default=None)
    parser.add_option('-p',dest='para',help='Injected parameter',default=None)
    (options,args) = parser.parse_args()
    if options.url==None:
        print 'please enter url'
    if options.data!=None and options.para!=None:
        pass
    else:
        print '[warning]: please enter data and para'
        sys.exit(0)
    return options

