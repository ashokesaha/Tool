import  sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSWidgets')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')

import nssrc.com.citrix.netscaler.nitro.service.nitro_service as NITROSVC
import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding as  VSRVRCKEY

try :
    ns = NITROSVC.nitro_service('10.102.28.201')
    ns.timeout = 5
    ns.set_credential('nsroot', 'nsroot')
    ns.login()
except Exception as e :
    print 'login failed : {}'.format(e.message)


try :
    vckey = VSRVRCKEY.sslvserver_sslcertkey_binding()
    vckey.vservername = 'one'
    vckey.certkeyname = 'TwoCA1024'
    vckey.ca = 'true'
    VSRVRCKEY.sslvserver_sslcertkey_binding.add(ns,vckey)
except Exception as e :
    print 'delete failed : {}'.format(e.message)

