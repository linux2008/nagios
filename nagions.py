#!/usr/bin/python

import os
import urllib,urllib2
import json
file=os.path.dirname(__file__)
conf=os.path.join(os.path.abspath(file),'hosts')
if not os.path.exists(conf):
    os.mkdir(conf)
host_temp="""define host {
           use       linux-server
           host_name %(hostname)s
           alias     %(hostname)s
           address   %(ip)s
}
"""
url=urllib2.urlopen('http://192.168.133.129:8000/hostinfo/getjson/')
data=json.loads(url.read())
conft=''
for i in data:
    for x in i['members']:
        conft+=host_temp %x

dir=os.path.join(conf,'host.cfg')
print dir
with open(dir,'w') as fd:
    fd.write(conft)
