import sys
import numpy as np
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')


from test_util      import *
from test_dut       import *
from test_config    import *
from curlClient     import *
from HttpServerCtrl import *

NSPYValidationErrStr = ' '


def NSPYClearErrStr() :
    global NSPYValidationErrStr
    NSPYValidationErrStr = ' '


def NSPYGetErrStr() :
    global NSPYValidationErrStr
    return NSPYValidationErrStr



def NSPYValidateNSIP(nsip) :
    global NSPYValidationErrStr
    NSPYValidationErrStr = ' '
    l = nsip.split()
    if(len(l) > 1) :
        NSPYValidationErrStr = 'Error: Only one DUT accepted'
        return False

    nsip = l[0]
    sess = Login(nsip, timeout=2)
    if not sess :
        NSPYValidationErrStr = 'Failed to login to DUT. Retry ...'
        return False

    sess = None
    return True



def NSPYValidateCurlClient(botip) :
    global NSPYValidationErrStr
    NSPYValidationErrStr = ' '

    cl = curlClient(botip, 2346)
    if not cl :
        NSPYValidationErrStr = 'Bad Bot ...'
        return None
    if not cl.Connect(timeout=2.0) :
        NSPYValidationErrStr = 'Bad Bot ...'
        return None
    return cl



def NSPYValidateBEServer(ip) :
    global NSPYValidationErrStr
    NSPYValidationErrStr = ' '

    beS = HttpServerCtrl(ip)
    if not beS :
        print 'NSPYValidateBEServer : err 1'
        NSPYValidationErrStr = 'Cannot create BE Server ...'
        return None
    if not beS.connect() :
        print 'NSPYValidateBEServer : err 2'
        NSPYValidationErrStr = 'Cannot connect BE Server ...'
        return None
    if not beS.sanitize() :
        print 'NSPYValidateBEServer : err 3'
        NSPYValidationErrStr = 'Cannot sanitize BE Server ...'
        return None
    return beS
    
        

