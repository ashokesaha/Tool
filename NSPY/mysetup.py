import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')


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


from ssltest.backend.BECipherIter import *
BECipherIter.Test()

#from curlClient import *
#curlClient.Test()


