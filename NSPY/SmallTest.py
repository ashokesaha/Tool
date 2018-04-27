import  sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSWidgets')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')

import nssrc.com.citrix.netscaler.nitro.service.nitro_service as NITROSVC
import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding as  VSRVRCKEY

import numpy as np

##ll = ['one','one','three','three','one','two','three','four',
##      'one','two','three','one','one','two','five','four',
##      'two','five','five','three']


ll = ['two','two','two','two',
      'two','two','two','two',
      'two','two','two','five',
      'one','two','three','four']

d = {}

for l in ll :
    try :
        d[l] = d[l] + 1
    except KeyError as e :
        d[l] = 1

dP = {}
for keys in d.keys() :
    dP[keys] = float(d[keys])/len(ll)

dPL = {}
for keys in dP.keys() :
    dPL[keys] = np.log2(dP[keys])



#print d
#print dP
#print dPL
etp = -sum(dPL.values())
print '{} -> {}'.format(d,etp)

