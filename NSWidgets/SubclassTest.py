import sys
import os
import random
import httplib
import json
import socket
import numpy as np
import scipy as sp
from PyQt5 import QtCore, QtWidgets, QtGui



class A (QtWidgets.QWidget) :
    def  __init__(self, parent=None):
        super(self.__class__,self).__init__(parent)
        print 'class A inited'



class B (A) :
    def  __init__(self, parent=None):
        #super(self.__class__,self).__init__(parent)
        print 'class B inited'



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    a = A()
    b = B()
    b.show()
