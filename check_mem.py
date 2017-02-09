#!/usr/bin/python

from optparse import OptionParser
import sys

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

def getmem(f):
    with open(f) as fd:
        for line in fd:
            if line.startswith('MemFree'):
                mem=line.split()[1].strip()
    return int(mem)/1024
def main():
    options,args=opt()
    w=int(options.waring)
    c=int(options.critical)
    mem=getmem('/proc/meminfo')
    if mem > w:
        print 'ok',str(mem)+'MB'
        sys.exit(0)
    elif c<mem<=w:
        print 'WARING',str(mem)+'MB'
        sys.exit(1)
    elif mem < c:
        print 'CRITICAL',str(mem)+'MB'
        sys.exit(2)
    else:
        print 'UNKNOWN',str+(mem)+'MB'
        sys.exit(3)
if __name__=='__main__':
   main()
