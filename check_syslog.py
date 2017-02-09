#!/usr/bin/python

from optparse import OptionParser
from subprocess import Popen,PIPE
import shlex
import datetime
import operator
import sys
MONTH={'Jan':1,
       'Feb':2,
       'Mar':3,
       'Apr':4,
       'May':5,
       'Jun':6,
       'Jul':7,
       'Aug':8,
       'Sep':9,
       'Oct':10,
       'Nov':11,
       'Dec':12
}

def opt():
    parser=OptionParser('%Usage: %prog [-w WARING],[-c CRITICAL]')
    parser.add_option('-w','--waring',
                       dest='waring',
                       action='store',
                       default=5,
                       help='WARING')
    parser.add_option('-c','--critical',
                       dest='critical',
                       action='store',
                       default=10,
                       help='CRITICAL')
    options,args=parser.parse_args()
    return options,args 

def fun(f,n):
    cmd='tail -n %s %s' %(n,f)
    p=Popen(shlex.split(cmd),stdout=PIPE,stderr=PIPE)
    stdout,stderr=p.communicate()
    return stdout

def log(line):
    now=datetime.datetime.now()
    month,day,time=line.split()[:3]
    hour,minute,second=[int(i) for i in time.split(':')]
    logtime=datetime.datetime(now.year,MONTH[month],int(day),hour,minute,second)
    return logtime

def dict(k,d):
    if k in d:
        d[k]+=1
    else:
        d[k]=1

def parse(data):
    dic={}
    now=datetime.datetime.now()
    ten_ago=now-datetime.timedelta(minutes=10)
    data=[i for i in data.split('\n') if i]
    for line in data:
        logtime=log(line)    
        if logtime >=ten_ago:
            dict(str(logtime),dic)
    return dic
def main():
    options,args=opt()
    b=Popen('whoami',stdout=PIPE)
    user=b.stdout.read()
    w=int(options.waring)
    c=int(options.critical)
    line=c*600
    data=fun('/var/log/messages',line)
    dic=parse(data)
    if not dic:
        print 'okok'
        sys.exit(0)
    sorted_dic=sorted(dic.iteritems(),key=operator.itemgetter(1),reverse=True)[0]
    num=sorted_dic[1]
    if num <w:
        print 'ok',sorted_dic,user
        sys.exit(0)
    if w <=num <c:
        print 'waring',sorted_dic,user
        sys.exit(1)
    if num>=c:
        print 'critical',sorted_dic,user
        sys.exit(2)
    else:
        print 'unknown',sorted_dic
        sys.exit(3)
if __name__=='__main__':
    print main()
