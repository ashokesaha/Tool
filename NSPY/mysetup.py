import sys


sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')


from test_util import *
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice import sslservice as SSLSVC
import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION



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


def     Test10() :
    namelist = []
    slist = []
    sess    = Login('10.102.28.201')

    s       = NSSVC()
    s.ip    = '10.102.28.61'
    s.port  = 5551
    s.name  = 'ashoke-1'
    s.servicetype = 'SSL'
    slist.append(s)

    s       = NSSVC()
    s.ip    = '10.102.28.61'
    s.port  = 5552
    s.name  = 'ashoke-2'
    s.servicetype = 'SSL'
    slist.append(s)

    NSSVC.add(sess,slist)

    for s in slist :
        namelist.append(s.name)


    sslsvclist = SSLSVC.get(sess,namelist)
    for s in sslsvclist :
        print s.servicename
        s.ssl3 = 'DISABLED'
        s.dhfile = None
        s.cipherurl = None
        s.sslv2url = None
        s.clientcert = None
        s.commonname = None
        s.pushenctrigger = None
        s.dtlsprofilename = None
        s.sslprofile = None
        s.ersa = 'DISABLED'
        s.ersacount=0
    
    try :
        SSLSVC.update(sess,sslsvclist)
        #SSLSVC.update(sess,sslsvclist[1])
    except NITROEXCEPTION.nitro_exception as e:
        print e.message



from ssltest.backend.BECipherIter import *
BECipherIter.Test()

#from curlClient import *
#curlClient.Test()


