import sys


sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')


import test_util
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice import sslservice as SSLSVC
import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
from nssrc.com.citrix.netscaler.nitro.resource.stat.ssl.ssl_stats import *
from nssrc.com.citrix.netscaler.nitro.resource.stat.ns.nsmemory_stats import *
import ServerControl
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey   as sslcertkey
import nssrc.com.citrix.netscaler.nitro.resource.stat.ns.ns_stats        as ns_stats
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertchain_sslcertkey_binding as sslcertchain_sslcertkey_binding


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



def SSLStat() :
    sess = test_util.Login('10.102.28.201')
    r = ssl_stats.get(sess)
    print type(r)
    print len(r)
    print type(r[0])
    print 'ssltotdec {}'.format(r[0].ssltotdec)
    r = ssl_stats.get(sess)
    print 'ssltotdec {}'.format(r[0].ssltotdec)


def NSMemeStat() :
    sess = test_util.Login('10.102.28.201')
    r = nsmemory_stats.get(sess)
    print len(r)
    print type(r)
    print r[1].pool
    print 'Done'




def CertKey() :
    sess = test_util.Login('10.102.28.201')
    #ck = sslcertkey.sslcertkey.get(sess)
    #for c in ck :
    #    print '{}'.format(c.certkey)

    try :
        ck = sslcertchain_sslcertkey_binding.sslcertchain_sslcertkey_binding.get(sess,'Server2048_sha256')
        for c in ck :
            print '{}  {}'.format(c.linkcertkeyname,c.certkeyname)
    except Exception as e :
        print e.message

    print '\n'

    try :
        ck = sslcertchain_sslcertkey_binding.sslcertchain_sslcertkey_binding.get(sess,'ThreeCA2048')
        for c in ck :
            print '{}  {}'.format(c.linkcertkeyname,c.certkeyname)
    except Exception as e :
        print e.message

    

def  NSStats() :
    sess = test_util.Login('10.102.28.201')
    st = ns_stats.ns_stats.get(sess,'sys_cur_alloc_bm16_entries')
    print type(st)


CertKey()
    


