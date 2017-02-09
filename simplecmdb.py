#!/usr/bin/python
import urllib,urllib2
from subprocess import Popen,PIPE
import pickle
import json
def getIfconfig():
    p=Popen(['ifconfig'],stdout=PIPE)
    data=p.stdout.read()
    return data

def getDmi():
    p=Popen(['dmidecode'],stdout=PIPE)
    data=p.stdout.read()
    return data

def parseData(data):
    parsed_data=[]
    new_line=''
    data=[i for i in data.split('\n') if i]
    for line in data:
        if line[0].strip():
            parsed_data.append(new_line)
            new_line=line+'\n'
        else:
            new_line+=line+'\n'
    parsed_data.append(new_line)
    return [i for i in parsed_data if i]

def parseIfconfig(parsed_data):
    dic={}
    parsed_data=[i for i in parsed_data if not i.startswith('lo')]
    for lines in parsed_data:
        line_list=lines.split('\n')
        devname=line_list[0].split()[0]
        macaddr=line_list[0].split()[-1]
        ipaddr=line_list[1].split()[1].split(':')[1]
        dic['ip']=ipaddr
    return dic

 
def parseDmi(parsed_data):
    dic={}
    parsed_data=[i for i in parsed_data if i.startswith('System Information')]
    parsed_data=[i for i in parsed_data[0].split('\n')[1:] if i]
    dmi_dic=dict([i.strip().split(':') for i in parsed_data])    
    dic['vender']=dmi_dic['Manufacturer']
    dic['product']=dmi_dic['Product Name']
    dic['sn']=dmi_dic['Serial Number'][:17]
    return dic

def getHostname(f):
    with open(f) as fd:
        for line in fd:
            if line.startswith('HOSTNAME'):
                hostname=line.split('=')[1].strip()
                break
    return{'hostname':hostname}

def getOSver(f):
    with open(f) as fd:
        for line in fd:
            osver=line.strip()
            break
    return {'osver':osver}

def getCpu(f):
    num=0
    with open(f) as fd:
        for line in fd:
            if line.startswith('processor'):
                num+=1
            if line.startswith('model name'):
                cpu_model=line.split(':')[1].split()
                cpu_model=cpu_model[0]+' '+cpu_model[-1]
    return{'cpu_num':num,'cpu_model':cpu_model}

def getMemory(f):
    with open(f) as fd:
        for line in fd:
            if line.startswith('MemTotal'):
                mem=int(line.split()[1].strip())
                break
    mem="%s" %(mem/1024.0)+'M'
    return{'memory':mem}


if __name__=='__main__':
    dic={}
    data_ip=getIfconfig()
    parsed_data_ip=parseData(data_ip)
    ip=parseIfconfig(parsed_data_ip)
    data_dmi=getDmi()
    parsed_data_dmi=parseData(data_dmi)
    dmi=parseDmi(parsed_data_dmi)
    hostname=getHostname('/etc/sysconfig/network')
    osver=getOSver('/etc/issue')
    cpu=getCpu('/proc/cpuinfo')
    mem=getMemory('/proc/meminfo')
    dic.update(dmi)
    dic.update(hostname)
    dic.update(ip)
    dic.update(osver)
    dic.update(cpu)
    dic.update(mem)
    print dic
#    data=urllib.urlencode(dic)
    data=pickle.dumps(dic)
    req=urllib2.urlopen('http://192.168.133.129:8000/hostinfo/collect/',data)
    print req.read()
