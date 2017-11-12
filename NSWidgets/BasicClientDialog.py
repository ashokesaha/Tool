# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ashoke_client.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSWidgets')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')

import socket
import struct
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from TestException import *
import GenericContainer
import NestedDict


class BasicClientDialog(object):
    def  __init__(self,container) :
        self.container = container
        self.curDUT = container.GetCurDUT()

    def setupUi(self, dialog):
        self.dialog = dialog
        dialog.setObjectName("BasicClientDialog")
        dialog.resize(468, 409)
        dialog.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.267045, y1:0.318, x2:1, y2:1, stop:0.948864 rgba(93, 158, 158, 255), stop:1 rgba(255, 255, 255, 255));")

        self.gridLayout = QtWidgets.QGridLayout(dialog)
        self.gridLayout.setObjectName("gridLayout")

        self.lineedit_name = QtWidgets.QLineEdit(dialog)
        self.lineedit_name.setStyleSheet("background-color: rgb(238, 238, 238);")
        self.lineedit_name.setObjectName("lineedit_name")
        self.lineedit_name.setText('')
        self.gridLayout.addWidget(self.lineedit_name, 0, 0, 1, 1)

        self.lineedit_ip = QtWidgets.QLineEdit(dialog)
        self.lineedit_ip.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_ip.setObjectName("lineedit_ip")
        self.lineedit_ip.setText('')
        self.gridLayout.addWidget(self.lineedit_ip, 0, 1, 1, 1)


        self.lineedit_targetip = QtWidgets.QLineEdit(dialog)
        self.lineedit_targetip.setStyleSheet("background-color: rgb(238, 238, 238);")
        self.lineedit_targetip.setObjectName("lineedit_targetip")
        self.lineedit_targetip.setText('')
        self.gridLayout.addWidget(self.lineedit_targetip, 1, 0, 1, 1)

        self.lineedit_targetport = QtWidgets.QLineEdit(dialog)
        self.lineedit_targetport.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_targetport.setObjectName("lineedit_targetport")
        self.lineedit_targetport.setText('')
        self.gridLayout.addWidget(self.lineedit_targetport, 1, 1, 1, 1)

        self.lineedit_certfile = QtWidgets.QLineEdit(dialog)
        self.lineedit_certfile.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_certfile.setObjectName("lineedit_certfile")
        self.lineedit_certfile.setText('')
        self.gridLayout.addWidget(self.lineedit_certfile, 2, 0, 1, 2)

        self.lineedit_keyfile = QtWidgets.QLineEdit(dialog)
        self.lineedit_keyfile.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_keyfile.setObjectName("lineedit_keyfile")
        self.lineedit_keyfile.setText('')
        self.gridLayout.addWidget(self.lineedit_keyfile, 3, 0, 1, 2)

        self.lineedit_certchain = QtWidgets.QLineEdit(dialog)
        self.lineedit_certchain.setStyleSheet("background-color: rgb(239, 239, 239);")
        self.lineedit_certchain.setObjectName("lineedit_certchain")
        self.lineedit_certchain.setText('')
        self.gridLayout.addWidget(self.lineedit_certchain, 4, 0, 1, 2)


        self.lineedit_versionfilter = QtWidgets.QLineEdit(dialog)
        self.lineedit_versionfilter.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_versionfilter.setObjectName("lineedit_versionfilter")
        self.lineedit_versionfilter.setText('')
        self.gridLayout.addWidget(self.lineedit_versionfilter, 5, 0, 1, 1)

        self.lineedit_cipherfilter = QtWidgets.QLineEdit(dialog)
        self.lineedit_cipherfilter.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_cipherfilter.setObjectName("lineedit_cipherfilter")
        self.lineedit_cipherfilter.setText('')
        self.gridLayout.addWidget(self.lineedit_cipherfilter, 5, 1, 1, 2)

        self.lineedit_reusecount = QtWidgets.QLineEdit(dialog)
        self.lineedit_reusecount.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_reusecount.setObjectName("lineedit_reusecount")
        self.gridLayout.addWidget(self.lineedit_reusecount, 6, 0, 1, 1)

        self.lineedit_renegcount = QtWidgets.QLineEdit(dialog)
        self.lineedit_renegcount.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_renegcount.setObjectName("lineedit_renegcount")
        self.gridLayout.addWidget(self.lineedit_renegcount, 6, 1, 1, 1)

        self.lineedit_itercount = QtWidgets.QLineEdit(dialog)
        self.lineedit_itercount.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_itercount.setObjectName("lineedit_itercount")
        self.gridLayout.addWidget(self.lineedit_itercount, 6, 2, 1, 1)

        self.lineedit_childcount = QtWidgets.QLineEdit(dialog)
        self.lineedit_childcount.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineedit_childcount.setObjectName("lineedit_childcount")
        self.gridLayout.addWidget(self.lineedit_childcount, 6, 3, 1, 1)

        self.label_recboundary = QtWidgets.QLabel(dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_recboundary.setFont(font)
        self.label_recboundary.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_recboundary.setObjectName("label_recboundary")
        self.gridLayout.addWidget(self.label_recboundary, 7, 0, 1, 1)

        self.recboundary_comboBox = QtWidgets.QComboBox(dialog)
        self.recboundary_comboBox.setStyleSheet("background-color: rgb(236, 236, 236);")
        self.recboundary_comboBox.setObjectName("recboundary_comboBox")
        self.recboundary_comboBox.addItem("")
        self.recboundary_comboBox.addItem("")
        self.recboundary_comboBox.addItem("")
        self.recboundary_comboBox.addItem("")
        self.gridLayout.addWidget(self.recboundary_comboBox, 7, 1, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setStyleSheet("background-color: rgb(74, 236, 217);")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 2)

        self.retranslateUi(dialog)
        self.buttonBox.rejected.connect(self.reject)

        if (self.container.GetType() == GenericContainer.GenericContainer.TYPE_FE_OPENSSL_CLIENT):
            self.buttonBox.accepted.connect(self.acceptSave)
            obj = self.container.GetBackendObj()
            if  obj :
                self.FillFromObj(obj)
        else :
            self.buttonBox.accepted.connect(self.accept)



    def retranslateUi(self, BasicClientDialog):
        _translate = QtCore.QCoreApplication.translate
        BasicClientDialog.setWindowTitle(_translate("BasicClientDialog", "BasicClientDialog"))
        self.lineedit_reusecount.setPlaceholderText(_translate("BasicClientDialog", "Reuse Count"))
        self.label_recboundary.setText(_translate("BasicClientDialog", "Rec Boundary"))
        self.lineedit_versionfilter.setPlaceholderText(_translate("BasicClientDialog", "Version Filter"))
        self.lineedit_ip.setPlaceholderText(_translate("BasicClientDialog", "IP Address"))
        self.lineedit_certchain.setPlaceholderText(_translate("BasicClientDialog", "Cert chain file"))
        #self.lineedit_port.setPlaceholderText(_translate("BasicClientDialog", "Port"))
        self.lineedit_name.setPlaceholderText(_translate("BasicClientDialog", "Name"))
        self.lineedit_certfile.setPlaceholderText(_translate("BasicClientDialog", "Cert File"))
        self.lineedit_keyfile.setPlaceholderText(_translate("BasicClientDialog", "Key File"))
        self.lineedit_cipherfilter.setPlaceholderText(_translate("BasicClientDialog", "Cipher Filter"))
        self.lineedit_renegcount.setPlaceholderText(_translate("BasicClientDialog", "Reneg Count"))
        self.lineedit_itercount.setPlaceholderText(_translate("BasicClientDialog", "Iter Count"))
        self.lineedit_childcount.setPlaceholderText(_translate("BasicClientDialog", "Child Count"))

        self.recboundary_comboBox.setItemText(0, _translate("BasicClientDialog", "All Separate"))
        self.recboundary_comboBox.setItemText(1, _translate("BasicClientDialog", "[CC+CKE] [CCV]"))
        self.recboundary_comboBox.setItemText(2, _translate("BasicClientDialog", "All Together"))
        self.recboundary_comboBox.setItemText(3, _translate("BasicClientDialog", "[CC] [CKE+CCV]"))

        self.lineedit_targetip.setPlaceholderText(_translate("BasicClientDialog", "Target ip"))
        self.lineedit_targetport.setPlaceholderText(_translate("BasicClientDialog", "Target port"))



    def  accept(self) :

        try :
            e = self.BuildEntity()
            if not e :
                print 'entity creation failed'
                raise TestException(1)
            if not e.Connect() :
                print 'entity connect failed'
                raise TestException(1)


        except TestException as e :
            plt = self.lineedit_name.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.lineedit_name.setPalette(plt)
            self.lineedit_name.cursorPositionChanged.connect(self.cursorPositionChanged)
            return

        ew = self.container.AddEntity(e.entity_type)
        ew.SetBackendObj(e)
        e.sigStatus.connect(ew.slotStatus)
        self.dialog.accept()



    def acceptSave(self) :
        obj = self.container.GetBackendObj()
        obj.certfile = self.lineedit_certfile.text()
        obj.keyfile  = self.lineedit_keyfile.text()
        obj.certchainfile = self.lineedit_certchain.text()
        obj.versionfilter = self.lineedit_versionfilter.text()
        obj.cipherfilter =  self.lineedit_cipherfilter.text()
        obj.reusecount = int(self.lineedit_reusecount.text())
        obj.renegcount = int(self.lineedit_renegcount.text())
        obj.itercount  = int(self.lineedit_itercount.text())
        obj.childcount = int(self.lineedit_childcount.text())
        obj.recboundary = self.recboundary_comboBox.currentIndex()
      
        self.dialog.accept()
 


    def  reject(self) :
        self.dialog.reject()



    def GetCurDUT(self) :
        return self.curDUT


    def cursorPositionChanged(self,old,new) :
        plt = self.lineedit_name.palette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        self.lineedit_name.setPalette(plt)
        self.lineedit_name.cursorPositionChanged.disconnect()




    def BuildEntity(self) :
        try :
            reusecount = int(self.lineedit_reusecount.text())
        except ValueError as e :
            reusecount = 0

        try :
            renegcount = int(self.lineedit_renegcount.text())
        except ValueError as e :
            renegcount = 0

        try :
            itercount = int(self.lineedit_itercount.text())
        except ValueError as e :
            itercount = 0

        try :
            childcount = int(self.lineedit_childcount.text())
        except ValueError as e :
            childcount = 0


        
        entity = BasicClientEntity(self.lineedit_name.text(),
                                        self.lineedit_ip.text(),
                                        2345,
                                        self.lineedit_targetip.text(),
                                        int(self.lineedit_targetport.text()),
                                        self.lineedit_certfile.text(),
                                        self.lineedit_keyfile.text(),
                                        self.lineedit_certchain.text(),
                                        self.lineedit_versionfilter.text(),
                                        self.lineedit_cipherfilter.text(),
                                        reusecount,renegcount,
                                        itercount,childcount,
                                        self.recboundary_comboBox.currentIndex())
        return entity


    def FillFromObj(self,obj) :
        self.lineedit_name.setText(obj.name)
        self.lineedit_ip.setText(obj.ip)
        self.lineedit_targetip.setText(obj.targetip)
        self.lineedit_targetport.setText(str(obj.targetport))
        self.lineedit_certfile.setText(obj.certfile)
        self.lineedit_keyfile.setText(obj.keyfile)
        self.lineedit_certchain.setText(obj.certchainfile)
        self.lineedit_versionfilter.setText(obj.versionfilter)
        self.lineedit_cipherfilter.setText(obj.cipherfilter)
        self.lineedit_reusecount.setText(str(obj.reusecount))
        self.lineedit_renegcount.setText(str(obj.renegcount))
        self.lineedit_itercount.setText(str(obj.itercount))
        self.lineedit_childcount.setText(str(obj.childcount))
        self.recboundary_comboBox.setCurrentIndex(obj.recboundary)
        self.lineedit_name.setReadOnly(True)
        self.lineedit_targetip.setReadOnly(True)
        self.lineedit_targetport.setReadOnly(True)




    def GetDialog(self) :
        return self.dialog
    
        self.name = name
        self.ip = ip
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.certchainfile = certchainfile
        self.versionfilter = versionfilter
        self.cipherfilter = cipherfilter
        self.reusecount = reusecount
        self.renegcount = renegcount
        self.itercount = itercount
        self.childcount = childcount
        self.recboundary = recboundary
        self.entity_type = GenericContainer.GenericContainer.TYPE_FE_OPENSSL_CLIENT
        self.isrunning = False
        self.sd = None






#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
class BasicClientEntity(QtCore.QObject):
    sigStatus = QtCore.pyqtSignal(int)
        
    def __init__(self,name,ip,port,targetip,targetport,
                 certfile=None,keyfile=None,certchainfile=None,
                 versionfilter=None,cipherfilter=None,
                 reusecount=0,renegcount=0,itercount=0,childcount=1,
                 recboundary=0) :
        super(self.__class__,self).__init__()
        self.name = name
        self.ip = ip
        self.port = port
        self.targetip = targetip
        self.targetport = targetport
        self.certfile = certfile
        self.keyfile = keyfile
        self.certchainfile = certchainfile
        self.versionfilter = versionfilter
        self.cipherfilter = cipherfilter
        self.reusecount = reusecount
        self.renegcount = renegcount
        self.itercount = itercount
        self.childcount = childcount
        self.recboundary = recboundary
        self.entity_type = GenericContainer.GenericContainer.TYPE_FE_OPENSSL_CLIENT
        self.isrunning = False
        self.sd = None
        self.logFp = None
        self.isRemoved = False


    def GetName(self) :
        return self.name

    def GetType(self) :
        return self.entity_type


    def OpenLog(self) :
        name = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\'
        name = name + '_' + self.name + '_' +  str(self.entity_type) + '.log'
        self.logFp = open(name,'w')
        return self.logFp


    def OpenLogRd(self) :
        name = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\'
        name = name + '_' + self.name + '_' +  str(self.entity_type) + '.log'
        self.logFp = open(name,'r')
        return self.logFp



    def CloseLog(self) :
        if self.logFp :
            self.logFp.close()
            self.logFp = None


    def WriteLog(self,s) :
        self.logFp.write(s)


    def GetSockTimeout(self) :
        if not self.sd :
            return 0
        return self.sd.gettimeout()


    def SetSockTimeout(self,to) :
        if not self.sd :
            return
        self.sd.settimeout(to)


    def IsRunning(self) :
        return self.isrunning
    

    def ToJson(self) :
        d = dict()
        d['name'] = self.name
        d['ip'] =  self.ip
        d['port'] =  self.port
        d['targetip'] =  self.targetip
        d['targetport'] =  self.targetport
        d['cipher']   = self.cipherfilter
        d['version'] = self.versionfilter
        d['cipher'] = self.cipherfilter
        d['cert'] = self.certfile
        d['key'] = self.keyfile
        d['certlink'] = self.certchainfile
        d['reuse'] = self.reusecount
        d['reneg'] = self.renegcount
        d['iter'] = self.itercount
        if self.childcount > 0 :
            d['childcount'] = self.childcount
        else :
            d['childcount'] = 1
        d['recboundary'] = self.recboundary
        
        s = json.dumps(d)
        return s



    def ToFileStr(self) :
        js = self.ToJson()
        d = dict()
        d['type'] = GenericContainer.GenericContainer.TYPE_FE_OPENSSL_CLIENT
        d['val'] = js
        s = json.dumps(d)
        return s



    @classmethod
    def FromFileStr(cls,jstring,sess=None) :
        d = json.loads(jstring)
        d = json.loads(d['val'])
        o = BasicClientEntity(d['name'],d['ip'],d['port'],
                    d['targetip'], d['targetport'],
                    d['cert'], d['key'],d['certlink'],
                    d['version'],d['cipher'],
                    d['reuse'],d['reneg'],d['iter'],d['childcount'],
                    d['recboundary'])
        return o



    @classmethod
    def CheckBots(cls,subnet) :
        for i in range(2,254) :
            ip = subnet + '.' + str(i)
            b = BasicClientEntity('basic',ip,2345,'1.1.1.1',1111)
            if b.Connect(timeout=0.3) :
                print '{} Passed'.format(ip)
                b.Terminate()
            else :
                #print '{} Failed'.format(ip)
                pass




    def Connect(self, timeout=2.0) :
        ret = True
        try :
            self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sd.settimeout(timeout)
            self.sd.connect ((self.ip, 2345))

            str = 'twinkletwinkle'
            lstr = struct.pack(">I", len(str))
            self.sd.sendall(lstr)
            self.sd.sendall(str)

            data = self.ReadOnce()
            if not data :
                ret = False
                return ret

            if not data.__eq__('upabovethe'):
                ret = False
                return ret
            
        except socket.error as e :
            ret = False

        return ret



    def  ReadOnce(self) :
        try :
            data = self.sd.recv(4)
        except  socket.error as e  :
            data = None
        
        if not data :
            return None

        len = struct.unpack("<I",data)
        if(len[0] == 0) :
            return None

        try :
            data = self.sd.recv(len[0])
            if data == 'ENDD' :
                self.Stop()
                data = None
        except socket.error as e :
            data = None

        return data




    def  SendOnce(self) :
        if not self.sd :
            self.Connect()
        if not self.sd :
            print 'try again later..'
            return
        
        str = self.ToJson()
        lstr = struct.pack(">I", len(str))
        self.sd.sendall(lstr)
        self.sd.sendall(str)


    def Terminate(self) :
        str = ''
        lstr = struct.pack(">I", len(str))
        self.sd.sendall(lstr)
        self.sd.close()
        self.sd = None


    def Start(self) :
        if not self.isrunning :
            if not self.sd :
                self.Connect()
            
            self.SendOnce()
            self.isrunning = True
            self.sigStatus.emit(1)
        

    def Stop(self) :
        if self.isrunning :
            self.isrunning = False
            while self.isRemoved == False :
                time.sleep(0.1)
            
            self.Terminate()
            self.sigStatus.emit(0)


    # Not all bots has meaning for start and stop. Like BE Server. It
    # is always on. Only way to disble it is to delete it.
    # But client entities has start stop.

    def IsStartStop(self) :
        return True

    def IsResults(self) :
        return True

    def IsProperty(self) :
        return True


    #tw is a TableWidget to be formatted by this object.
    #The tw is part of a ResultDialog and it calls each object
    #to format the table accordingly.
    
    def PrepareResult(self) :
        fp = self.OpenLogRd()
        N = NestedDict.NestedDict()
        K = ['version','cipher','ServerCert']
        N.SetKeys(K)
        N.LoadFileFp(fp)
        tw = N.GetViewWidget(None)
        l = []
        N.Print(N.keys,l)
        return tw


if __name__ == "__main__":

    while True :
        BasicClientEntity.CheckBots('10.102.28')
    
    
##    b = BasicClientEntity('ashoke','10.102.28.1',4040,'certfile','keyfile',
##                          'certchainfile','TLS1.2','ECDHE')
##    app = QtWidgets.QApplication(sys.argv)
##    dialog = QtWidgets.QDialog()
##    Form = GenericContainer(GenericContainer.CONTAINER_L1)
##    ui = BasicClientDialog(Form)
##    ui.setupUi(dialog)
##    dialog.show()
##    sys.exit(app.exec_())

