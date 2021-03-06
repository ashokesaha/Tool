# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MasterContainer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSWidgets')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')
from   PyQt5 import QtCore, QtGui, QtWidgets
from   DUTDialog import *
from   CounterList import *
from   CustomWidget import *
import GenericContainer
import TestException
import AllocFree
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher as CIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslciphersuite as CIPHERSUITE




class LogReaderThread(QtCore.QThread) :
    
    def __init__(self) :
        super(self.__class__,self).__init__()
        self.objList = []
        self.sleeptime = 1.0


    def RegisterObj(self, obj) :
        obj.isRemoved = False
        self.objList.append(obj)


    def RemoveObj(self, obj) :
        if obj in self.objList :
            self.objList.remove(obj)
        obj.isRemoved = True


    def SetSleepTime(self, t) :
        self.sleeptime = float(t)


    def run(self) :
        while True :
            for o in self.objList :
                if not o.IsRunning() :
                    self.RemoveObj(o)
                    while not o.isRemoved :
                        QtCore.QThread.sleep(0.25)
                    continue
                t = o.GetSockTimeout()
                o.SetSockTimeout(0.1)
                s = o.ReadOnce()
                o.SetSockTimeout(t)

            QtCore.QThread.sleep(1)




class UpDownThread(QtCore.QThread) :
    updownSignal = QtCore.pyqtSignal(int)
    
    def __init__(self) :
        super(self.__class__,self).__init__()
        self.containerList = []
        self.sleeptime = 3

    def AddContainer(self,o) :
        self.containerList.append(o)

    def RemoveContainer(self,o) :
        self.containerList.remove(o)
    
    def run(self) :
        while True :
            for c in self.containerList :
                for e in c.entityList :
                    o = e.GetBackendObj()
                    o.Refresh()
            
            self.updownSignal.emit(1)
            QtCore.QThread.sleep(self.sleeptime)




class MasterContainer(QtWidgets.QWidget):

    pollThread = LogReaderThread()
    pollThread.start()
    updownThread = UpDownThread()
    updownThread.start()


    def  __init__(self, parent=None):
        super(self.__class__,self).__init__(parent)
        self.DUTList = []
        self.CurDUT  = None
        self.SSLBEServerList = []

    
    def setupUi(self):
        Form.setObjectName("Form")
        Form.resize(800, 573)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(1,1,1,1)
        self.horizontalLayout.setSpacing(2)
        
        self.L1 = GenericContainer.GenericContainer(GenericContainer.GenericContainer.CONTAINER_L1,self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L1.sizePolicy().hasHeightForWidth())
        self.L1.setSizePolicy(sizePolicy)
        self.L1.setObjectName("L1")
        self.horizontalLayout.addWidget(self.L1)
        self.L1.show()
        
        
        self.L2 = GenericContainer.GenericContainer(GenericContainer.GenericContainer.CONTAINER_L2,self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L2.sizePolicy().hasHeightForWidth())
        self.L2.setSizePolicy(sizePolicy)
        self.L2.setAccessibleDescription("")
        self.L2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.L2.setObjectName("L2")
        self.horizontalLayout.addWidget(self.L2)

        
        self.T1_NS = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.T1_NS.sizePolicy().hasHeightForWidth())
        self.T1_NS.setSizePolicy(sizePolicy)
        self.T1_NS.setObjectName("T1_NS")

        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.T1_NS)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(2)
        
        self.T1 = GenericContainer.GenericContainer(GenericContainer.GenericContainer.CONTAINER_T1,self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.T1.sizePolicy().hasHeightForWidth())
        self.T1.setSizePolicy(sizePolicy)
        self.T1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.T1.setObjectName("T1")

        self.verticalLayout.addWidget(self.T1)


        self.NSHOLDER = MyRectWidget(GenericContainer.GenericContainer.CONTAINER_NSHOLDER,self.T1_NS)
        self.NSHOLDER.verticalLayout = QtWidgets.QVBoxLayout(self.NSHOLDER)
        self.NSHOLDER.verticalLayout.setSpacing(2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(8)
        sizePolicy.setHeightForWidth(self.NSHOLDER.sizePolicy().hasHeightForWidth())
        self.NSHOLDER.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.NSHOLDER)


        self.NS1 = NSWidget(ccode=1)
        self.NS1.setObjectName("NS1")
        self.NS1.SetContainer(self)
        self.NSHOLDER.verticalLayout.addWidget(self.NS1)
 
        self.NS2 = NSWidget(ccode=2)
        self.NS2.setObjectName("NS2")
        self.NS2.SetContainer(self)
        self.NSHOLDER.verticalLayout.addWidget(self.NS2)

        self.NS3 = NSWidget(ccode=3)
        self.NS3.setObjectName("NS3")
        self.NS3.SetContainer(self)
        self.NSHOLDER.verticalLayout.addWidget(self.NS3)

        self.NS4 = NSWidget(ccode=4)
        self.NS4.setObjectName("NS4")
        self.NS4.SetContainer(self)
        self.NSHOLDER.verticalLayout.addWidget(self.NS4)


        self.L2.raise_()
        self.T1.raise_()
        #self.NS.raise_()
        self.NSHOLDER.raise_()
        self.T1_NS.raise_()
        self.horizontalLayout.addWidget(self.T1_NS)

        
        self.R2 = GenericContainer.GenericContainer(GenericContainer.GenericContainer.CONTAINER_R2,self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.R2.sizePolicy().hasHeightForWidth())
        self.R2.setSizePolicy(sizePolicy)
        self.R2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.R2.setObjectName("R2")
        self.R2.setAcceptDrops(True)
        self.T1_NS.raise_()
        self.horizontalLayout.addWidget(self.R2)

        
        self.R1 = GenericContainer.GenericContainer(GenericContainer.GenericContainer.CONTAINER_R1,self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.R1.sizePolicy().hasHeightForWidth())
        self.R1.setSizePolicy(sizePolicy)
        self.R1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.R1.setObjectName("R1")
        self.horizontalLayout.addWidget(self.R1)



        self.B = GenericContainer.GenericContainer(GenericContainer.GenericContainer.CONTAINER_BOT,self)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.B.sizePolicy().hasHeightForWidth())
        self.B.setSizePolicy(sizePolicy)
        self.B.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.B.setObjectName("B")
        self.horizontalLayout.addWidget(self.B)


        sizePolicy2 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)        
        sizePolicy2.setVerticalStretch(5)
        sizePolicy2.setHorizontalStretch(1)
        self.B.lw = QtWidgets.QListWidget(None)
        self.B.lw.setSortingEnabled(True)
        self.B.lw.setSpacing(2)
        self.B.isProbing = False
        self.B.lw.setSizePolicy(sizePolicy2)


        sizePolicy3 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)        
        sizePolicy.setHorizontalStretch(1)
        self.B.le = QtWidgets.QLineEdit(None)
        self.B.le.setSizePolicy(sizePolicy3)


        sizePolicy4 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(1)
        self.B.pb = QtWidgets.QPushButton(None)
        self.B.pb.setSizePolicy(sizePolicy4)
        self.B.pb.setText('Provision')

        self.B.myLayout.setSpacing(10)
        self.B.myLayout.addWidget(self.B.lw)
        self.B.myLayout.addWidget(self.B.le)
        self.B.myLayout.addWidget(self.B.pb)
        self.B.le.raise_()

        self.B.pb.clicked.connect(self.ProvisionIP)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.L1.setAccessibleDescription(_translate("Form", "L1"))
        self.L2.setAccessibleName(_translate("Form", "L2"))
        self.T1.setAccessibleName(_translate("Form", "T1"))
        self.R2.setAccessibleName(_translate("Form", "R2"))
        self.R1.setAccessibleName(_translate("Form", "R1"))

        self.updownThread.updownSignal.connect(self.UpDownUpdate)
        self.updownThread.AddContainer(self.L2)
        self.updownThread.AddContainer(self.R2)



    def UpDownUpdate(self, i) :
        for w in self.L2.entityList :
            w.update()
            
        for w in self.R2.entityList :
            w.update()



    def GetCurDUT(self) :
        return self.CurDUT


    def SetCurDUT(self,dut) :
        if dut not in self.DUTList :
            return

        self.NS1.isActive = False
        self.NS2.isActive = False
        self.NS3.isActive = False
        self.NS4.isActive = False
        
        if self.NS1.GetBackendObj() == dut :
            self.NS1.isActive = True
        elif self.NS2.GetBackendObj() == dut :
            self.NS2.isActive = True
        if self.NS3.GetBackendObj() == dut :
            self.NS3.isActive = True
        elif self.NS4.GetBackendObj() == dut :
            self.NS4.isActive = True

        self.NS1.update()
        self.NS2.update()
        self.NS3.update()
        self.NS4.update()
        
        self.CurDUT = dut
        

    def AddDUT(self,dut) :
        if dut not in self.DUTList :
            self.DUTList.append(dut)
            self.SetCurDUT(dut)
    

    def GetSess(self) :
        return self.NS.GetSess()


    def AddToSSLBEServerList(self,e) :
        self.SSLBEServerList.append(e)


    def ReplaceNSWithCounterList(self) :
        NSCounterList.Init()

        F = FetcherThread('10.102.28.201', freq=0)
        F.AddCounters(NSCounterList.COUNTERS)
        F.Chunkify(5)

        w = NSCounterHarnessWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.NS.sizePolicy().hasHeightForWidth())
        w.setSizePolicy(sizePolicy)

        w.SetFetcherThread(F)
        w.AddCounter('ssl_cur_sslInfo_SPCBInUseCount')
        w.AddCounter('pcb_cur_inuse')
        w.SetXYScale(5.0,0.1)
        w.SetFromToTicks(0,100)

        self.verticalLayout.replaceWidget(self.NS, w)


    def GetDUTByIP(self,nsip) :
        for dut in self.DUTList :
            if dut.nsip == nsip :
                return dut

        return None



    def GetCounterWidget(self) :
        NSCounterList.Init()
        F = FetcherThread('10.102.28.201', freq=0)
        F.AddCounters(NSCounterList.COUNTERS)
        F.Chunkify(5)
        w = NSCounterHarnessWidget()

        w.SetFetcherThread(F)
        w.AddCounter('ssl_cur_sslInfo_SPCBInUseCount')
        w.AddCounter('pcb_cur_inuse')
        w.SetXYScale(5.0,0.1)
        w.SetFromToTicks(0,100)

        return w



    def ProvisionIP(self, b) :
        print 'ProvisionIP called with {}'.format(self.B.le.text())
        ip = self.B.le.text()
        if not ip :
            return
        if len(ip) == 0 :
            return

        try :
            clnt = paramiko.client.SSHClient()
            clnt.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            clnt.connect(ip, username='root', password='freebsd', timeout=2.0)
            sftp = clnt.open_sftp()
            d = '/tmp/botify'
            s = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\botify'
            sftp.put(s,d)

            cmdstr  = 'chmod +x /tmp/botify; /tmp/botify'
            fin,fout,ferr = clnt.exec_command(cmdstr)

            print 'Printing output :'
            for l in fout :
                print l
            print 'Printing error :'
            for l in ferr :
                print l
            
        except socket.error :
            print 'Failed to provision {}'.format(ip)
            return
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = MasterContainer()
    Form.setupUi()
    Form.show()
    sys.exit(app.exec_())



