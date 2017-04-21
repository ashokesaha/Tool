import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke\\nitro-python-1.0')

import pip

try :
    import requests
except :
    l = 'install requests'.split()
    pip.main(l)

try :
    import paramiko
except :
    l = 'install paramiko'.split()
    pip.main(l)


import HttpServerCtrl
reload(HttpServerCtrl)
from HttpServerCtrl import *

import curlClient
reload(curlClient)


#clnt = HttpServerCtrl('10.102.28.61')
#clnt.connect()

#clnt.StartStop(1)
#n = clnt.NumProcess('httpd')
#print 'num of httpd is {}'.format(n)

#sys.stdin.readline()
#clnt.StartStop(0)
#n = clnt.NumProcess('httpd')
#print 'num of httpd is {}'.format(n)



#lset = clnt.LinkSet()
#lnk = lset.next()
#sys.stdin.readline()
#lnk = lset.next()
#sys.stdin.readline()
#lnk = lset.next()
#sys.stdin.readline()


#print lnk
#clnt.StartStop(1)
#clnt.ferr.read()

