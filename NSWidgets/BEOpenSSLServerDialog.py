# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BEOpenSSLServerDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import socket
import struct
import json
import time
from PyQt5            import QtCore, QtGui, QtWidgets
import GenericContainer
from TestException    import *
import NestedDict

class BEOpenSSLServerDialog(object):
    def  __init__(self,container) :
        self.container = container

    
    def setupUi(self, dialog):
        self.dialog = dialog
        dialog.setObjectName("dialog")
        dialog.resize(400, 300)
        dialog.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(93, 158, 158, 255), stop:1 rgba(255, 255, 255, 255));")
        self.gridLayout = QtWidgets.QGridLayout(dialog)
        self.gridLayout.setObjectName("gridLayout")
        
        self.lineEdit = QtWidgets.QLineEdit(dialog)
        self.lineEdit.setStyleSheet("border-color: rgb(255, 85, 0);\n"
"background-color: rgb(244, 244, 244);")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        
        self.lineEdit_2 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_2.setStyleSheet("background-color: rgb(247, 247, 247);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        self.lineEdit_3 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_3.setStyleSheet("background-color: rgb(244, 244, 244);")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 0, 2, 1, 1)

        self.comboBox4 = QtWidgets.QComboBox(dialog)
        self.comboBox4.setStyleSheet("background-color: rgb(236, 236, 236);")
        self.comboBox4.setObjectName("responseprofile_comboBox")
        self.comboBox4.addItem("Profile One")
        self.comboBox4.addItem("Profile Two")
        self.gridLayout.addWidget(self.comboBox4, 1, 0, 1, 1)


        self.lineEdit_5 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_5.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout.addWidget(self.lineEdit_5, 1, 1, 1, 1)

        self.lineEdit_6 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_6.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout.addWidget(self.lineEdit_6, 1, 2, 1, 1)

        self.lineEdit_7 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_7.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout.addWidget(self.lineEdit_7, 2, 0, 1, 1)

        self.lineEdit_8 = QtWidgets.QLineEdit(dialog)
        #self.lineEdit_8.setEnabled(False)
        self.lineEdit_8.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout.addWidget(self.lineEdit_8, 2, 1, 1, 1)

        self.lineEdit_9 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_9.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.gridLayout.addWidget(self.lineEdit_9, 2, 2, 1, 1)

        self.checkBox = QtWidgets.QCheckBox(dialog)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 0, 1, 1)

        self.checkBox_2 = QtWidgets.QCheckBox(dialog)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 3, 1, 1, 1)

        self.checkBox_3 = QtWidgets.QCheckBox(dialog)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 3, 2, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)

        self.retranslateUi(dialog)
        self.buttonBox.rejected.connect(self.reject)

        if (self.container.GetType() == GenericContainer.GenericContainer.TYPE_BE_OPENSSL_SERVER):
            self.buttonBox.accepted.connect(self.acceptSave)
            obj = self.container.GetBackendObj()
            if  obj :
                self.FillFromObj(obj)
        else :
            self.buttonBox.accepted.connect(self.accept)



    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "BE OpenSSL Server"))
        self.lineEdit.setPlaceholderText(_translate("dialog", "Name"))
        self.lineEdit_2.setPlaceholderText(_translate("dialog", "IP Address"))
        self.lineEdit_3.setPlaceholderText(_translate("dialog", "Port"))
        self.lineEdit_5.setPlaceholderText(_translate("dialog", "Record size"))
        self.lineEdit_6.setPlaceholderText(_translate("dialog", "Inter Record Delay"))
        self.lineEdit_7.setPlaceholderText(_translate("dialog", "Cipher Filter"))
        self.lineEdit_8.setPlaceholderText(_translate("dialog", "Response size"))
        self.lineEdit_9.setPlaceholderText(_translate("dialog", "toPort"))
        self.checkBox.setText(_translate("dialog", "Reuse"))
        self.checkBox_2.setText(_translate("dialog", "Reneg"))
        self.checkBox_3.setText(_translate("dialog", "CAuth"))



    def  accept(self) :
        eList = []
        try :
            try :
                fromPort = int(self.lineEdit_3.text())
            except ValueError as e :
                print 'Bad fromPort'
                raise TestException()

            try :
                toPort = int(self.lineEdit_9.text())
            except ValueError as e :
                print 'Bad toPort'
                toPort = fromPort
            
            if fromPort > toPort :
                print 'invalid toPort'
                raise TestException()


            while fromPort <= toPort :    
                e = self.BuildEntity(fromPort)
                fromPort += 1
                if not e :
                    print 'entity creation failed'
                    continue
                if not e.Connect() :
                    print 'entity connect failed'
                    continue

                eList.append(e)

        except TestException as e :
            plt = self.lineEdit.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.lineEdit.setPalette(plt)
            self.lineEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
            return

        for e in eList :
            ew = self.container.AddEntity(e.entity_type)
            ew.SetBackendObj(e)
            self.AddToSSLBEServerList(e)
            e.sigStatus.connect(ew.slotStatus)
            e.Start()

        self.dialog.accept()
        


    def AddToSSLBEServerList(self,e) :
        self.container.AddToSSLBEServerList(e)


    def acceptSave(self) :

        try :
            recsize = int(self.lineEdit_5.text())
        except ValueError as e :
            recsize = 512

        try :
            delay = int(self.lineEdit_6.text())
        except ValueError as e :
            delay = 0

        try :
            respsize = int(self.lineEdit_8.text())
        except ValueError as e :
            respsize = 512

        
        obj = self.container.GetBackendObj()
        obj.resp_profile = self.comboBox4.currentIndex()
        obj.record_size = self.lineEdit_5.text()
        obj.record_delay = self.lineEdit_6.text()
        obj.cipher_filter = self.lineEdit_7.text()
        obj.reuse = self.checkBox.isChecked()
        obj.reneg = self.checkBox_2.isChecked()
        obj.cauth = self.checkBox_3.isChecked()
        obj.resp_size = respsize
        obj.record_size = recsize
        obj.inter_record_delay = delay


        obj.SendOnce()
        self.dialog.accept()



    def  reject(self) :
        self.dialog.reject()



    def cursorPositionChanged(self,old,new) :
        plt = self.lineEdit.palette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        self.lineEdit.setPalette(plt)
        self.lineEdit.cursorPositionChanged.disconnect()



    def BuildEntity(self, port = 0) :
        if port :
            portStr = str(port)
            nameStr = self.lineEdit.text() + '_' + portStr
        else :
            portStr = self.lineEdit_3.text()
            nameStr = self.lineEdit.text()


        try :
            recsize = int(self.lineEdit_5.text())
        except ValueError as e :
            recsize = 512

        try :
            delay = int(self.lineEdit_6.text())
        except ValueError as e :
            delay = 0

        try :
            respsize = int(self.lineEdit_8.text())
        except ValueError as e :
            respsize = 512

        
        
        entity = BEOpenSSLServerEntity(nameStr,
                                       self.lineEdit_2.text(),
                                       portStr,
                                       self.comboBox4.currentIndex(),
                                       recsize,
                                       delay,
                                       self.lineEdit_7.text(),
                                       self.checkBox.isChecked(),
                                       self.checkBox_2.isChecked(),
                                       self.checkBox_3.isChecked(),
                                       respsize)
        return entity


    def FillFromObj(self,obj) :
        print 'BEOpenSSLServer: FillFromObj :...'
        
        self.lineEdit.setText(obj.name)
        self.lineEdit_2.setText(obj.ip)
        self.lineEdit_3.setText(obj.listen_port)
        self.comboBox4.setCurrentIndex(obj.resp_profile)
        self.lineEdit_5.setText(str(obj.record_size))
        self.lineEdit_6.setText(str(obj.inter_record_delay))
        self.lineEdit_7.setText(obj.cipher_filter)
        self.lineEdit_8.setText(str(obj.resp_size))

        if obj.reuse :
            self.checkBox.setCheckState(2)
        else :
            self.checkBox.setCheckState(0)

        if obj.reneg :
            self.checkBox_2.setCheckState(2)
        else :
            self.checkBox_2.setCheckState(0)
        
        if obj.cauth :
            self.checkBox_3.setCheckState(2)
        else :
            self.checkBox_3.setCheckState(0)


        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
    

    def GetDialog(self) :
        return self.dialog
    
    
#
#
#
#
#
class BEOpenSSLServerEntity(QtCore.QObject):
    sigStatus = QtCore.pyqtSignal(int)

    #=====================================================#
    def __init__(self,name,ip,port,resp_profile,record_size,delay,cipher_filter,reuse,reneg,cauth,resp_size) :
        super(self.__class__,self).__init__()
        self.name = name
        self.ip = ip
        self.listen_port = port
        self.type = 'SSL'
        self.resp_size = int(resp_size)
        self.resp_profile = resp_profile
        self.record_size = record_size
        self.inter_record_delay = delay
        self.cipher_filter = cipher_filter
        self.reuse = reuse
        self.reneg = reneg
        self.cauth = cauth
        self.inter_record_delay = delay
        self.entity_type = GenericContainer.GenericContainer.TYPE_BE_OPENSSL_SERVER
        self.sd = None
        self.isrunning = False
        self.isRemoved = False
        self.ReadOnceCount = 1


    #=====================================================#
    def GetType(self) :
        return self.entity_type


    def GetName(self) :
        s = self.ip + '\n' + str(self.listen_port)
        return s



    #=====================================================#
    def ToJson(self) :
        d = dict()
        d['name']           = self.name
        d['ip']             = self.ip
        d['listen_port']    = self.listen_port
        d['resp_profile']   = self.resp_profile
        d['record_size']    = self.record_size
        d['resp_size']      = self.resp_size
        d['cipher_filter']  = self.cipher_filter
        d['inter_record_delay'] = self.inter_record_delay 
        d['reuse']          = self.reuse
        d['reneg']          = self.reneg
        d['cauth']          = self.cauth
        d['delay']          = self.inter_record_delay
        s = json.dumps(d)
        return s


    def ToFileStr(self) :
        js = self.ToJson()
        d = dict()
        d['type'] = GenericContainer.GenericContainer.TYPE_BE_OPENSSL_SERVER
        d['val'] = js
        s = json.dumps(d)
        return s


    @classmethod
    def FromFileStr(cls,jstring) :
        d = json.loads(jstring)
        d = json.loads(d['val'])
        o =  BEOpenSSLServerEntity(d['name'], d['ip'], d['listen_port'],
                                   d['resp_profile'],d['record_size'],
                                   d['delay'],d['cipher_filter'],
                                   d['reuse'],d['reneg'],d['cauth'],d['resp_size'])

        return o



    #=====================================================#
    def Connect(self, timeout=2.0) :
        ret = True
        try :
            self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sd.settimeout(timeout)
            self.sd.connect ((self.ip, 2347))

            str = 'twinkletwinkle'
            lstr = struct.pack(">I", len(str))
            self.sd.sendall(lstr)
            self.sd.sendall(str)

            data = self.ReadOnce()
            if not data :
                ret = False
                return ret
            
            if not data.__eq__('howiwonder'):
                ret = False
                return ret
            
        except socket.error as e :
            print 'BEOpenSSLServerEntity: Connect. Exception happened'
            ret = False

        return ret


    #=====================================================#
    def  ReadOnce(self) :
        try :
            data = self.sd.recv(4)
        except  socket.error as e  :
             data = None
        
        if not data :
            return None

        ll = struct.unpack("<I",data)
        if(ll[0] == 0) :
            return None
        
        if(ll[0] > 1024) :
            print 'ReadOnce ({}) big len. returning'.format(ll[0])
            return None

        
        try :
            data = self.sd.recv(ll[0])
            print data
            
        except socket.error as e :
            data = None

        return data


    #=====================================================#
    def  SendOnce(self) :
        if not self.sd :
            self.Connect()
        
        str = self.ToJson()
        lstr = struct.pack(">I", len(str))

        doretry=0
        try :
            self.sd.sendall(lstr)
        except socket.error as e :
            doretry = 1

        if doretry :
            QtCore.QThread.sleep(1)
            self.sd.sendall(lstr)
            doretry = 0

        try :
            self.sd.sendall(str)
        except socket.error as e :
            doretry = 1

        if doretry :
            QtCore.QThread.sleep(1)
            self.sd.sendall(str)
            doretry=0


    def AskResult(self) :
        d = dict()
        d['result'] = 1
        s = json.dumps(d)
        lstr = struct.pack(">I", len(s))
        if not self.sd :
            self.Connect()
        
        self.sd.sendall(lstr)
        self.sd.sendall(s)



    #=====================================================#
    def Terminate(self) :
        str = ''
        lstr = struct.pack(">I", len(str))
        doretry = 0
        try :
            self.sd.sendall(lstr)
            self.sd.close()
            self.sd = None
        except socket.error as e :
            doretry = 1

        if doretry :
            self.Connect()
            self.sd.sendall(lstr)
            self.sd.close()
            self.sd = None
    


    def GetSockTimeout(self) :
        if not self.sd :
            return 0
        return self.sd.gettimeout()


    def SetSockTimeout(self,to) :
        if not self.sd :
            return
        self.sd.settimeout(to)



    # Not all bots has meaning for start and stop. Like BE Server. It
    # is always on. Only way to disble it is to delete it.
    # But client entities has start stop.
    def IsStartStop(self) :
        return True

    def IsRunning(self) :
        return self.isrunning

    def IsResults(self) :
        return True

    def IsProperty(self) :
        return True


    def Start(self) :
        if not self.isrunning :
            if not self.sd :
                self.Connect()
            self.SendOnce()
            self.isrunning = True
            self.sigStatus.emit(1)

        

    def Stop(self) :
        if not self.sd :
            self.isrunning = False
            self.sigStatus.emit(0)
        if self.isrunning :
            self.isrunning = False
            self.Terminate()
            self.sigStatus.emit(0)


    def OpenLog(self) :
        name = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\'
        name = name + '_' + self.name + '_' +  str(self.entity_type) + '.log'
        self.logFp = open(name,'w')
        return self.logFp


    def OpenLogRd(self) :
        name = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\'
        name = name + '_' + self.name + '_' +  str(self.entity_type) + '.log'
        self.logFp = open(name,'r')
        print 'opening log {}'.format(name)
        return self.logFp


    def CloseLog(self) :
        if self.logFp :
            self.logFp.close()
            self.logFp = None


    def WriteLog(self,s) :
        self.logFp.write(s)




    #tw is a TableWidget to be formatted by this object.
    #The tw is part of a ResultDialog and it calls each object
    #to format the table accordingly.
    
    def PrepareResult(self) :
        N = NestedDict.NestedDict()
        K = ['a','version','cipher','ServerCert','ClientCert','ECC']
        K = ['version','cipher','ServerCert','ClientCert','ECC','DH']
        N.SetKeys(K)
        L = []
        

        self.AskResult()
        while True :
            s = self.ReadOnce()
            if not s :
                break;
            try :
                d = json.loads(s)
                N.AddDict(d)
            except ValueError as e :
                print 'bad json {}'.format(s)
        
        tw = N.GetViewWidget(None)
        l = []
        N.Print(N.keys,l)
        return tw


    def PrepareMimeData(self,ccode=None) :
        print 'PrepareMimeData for BEOpenSSLServer . entity_type {}'.format(self.entity_type)
        d = dict()
        d['name'] = self.name
        d['type'] = self.entity_type
        d['ip'] = self.ip
        d['port'] = self.listen_port
        s = json.dumps(d)
        return s
    

    def AllowDrop(self,jstring) :
        return False


    def __del__(self) :
        print 'entity deleted {}'.format(self)



  

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = BEOpenSSLServerDialog(4)
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

