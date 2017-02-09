#!/usr/bin/python

from optparse import OptionParser
import sys

unit={'b':1,'k':2**10,'m':2**20,'g':2**30,'t':2**40}
def opt():
    parser=OptionParser("usage:%prog, [-w WARING] [-c CRITIAL]")
    parser.add_option('-w','--waring',
                       dest='waring',
                       action='store',
                       default='100',
                       help='WARING')
    parser.add_option('-c','--critical',
                       dest='critical',
                       action='store',
                       default='50',
                       help='CRITICAL')
    options,args=parser.parse_args()
    return options,args

def units(s):
    last=s[:-1]
    last=last.lower()
    num=float(s[:-1])
    if last in unit:
        return num*unit[last]
    else:
        return int(s)
def change(byte):
    for k,v in unit.items():
        num1=float(byte)/v
        if 0<num1<=1:
            num1='%.2f' %num1
            result=str(num1)+k.upper()
    return result

def getmem(f):
    with open(f) as fd:
        for line in fd:
            if line.startswith('MemFree'):
                mem=line.split()[1].strip()
    return int(mem)*1024

def main():
    options,args=opt()
    w=units(options.waring)
    c=units(options.critical)
    mem=getmem('/proc/meminfo')
    read=change(mem)
    if mem > w:
        print 'OK',read
        sys.exit(0)
    elif c<mem<=w:
        print 'WARING',read
        sys.exit(1)
    elif mem < c:
        print 'CRITICAL',read
        sys.exit(2)
    else:
        print 'UNKNOWN',read
        sys.exit(3)
if __name__=='__main__':
    main()
