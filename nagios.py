#!/usr/bin/python
import os,sys
import urllib,urllib2
import json
dir=os.path.dirname(__file__)
conf=os.path.join(os.path.abspath(dir),'host')
try:
    if not os.path.exists('conf'):
        os.mkdir(conf)
except:
    print 'it is exists'

temp=''' define host {
                     use           linux_server
                     host_name    %(hostname)s
                     alias        %(hostname)s
                     address      %(ip)s
  }
'''
con=''
url=urllib2.urlopen('http://192.168.133.129:8000/hostinfo/getjson/')
data=json.loads(url.read())
for i in data:
    for a in i['members']:
        con+=temp %a

dirs=os.path.join(conf,'hosts.cfg')
with open(dirs,'w') as fd:
    fd.write(con)



