import  sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSWidgets')
from    PyQt5 import QtCore, QtGui, QtWidgets
import  CustomWidget
import  CertInstaller
from    BEOpenSSLServerDialog import *
from    BasicClientDialog     import *
from    DUTDialog             import *
from    ocsp_responder        import *


if __name__ == "__main__":
    print 'BasicClientDialog {}  '.format(type(BasicClientDialog))
    b = BEOpenSSLServerDialog(None)
