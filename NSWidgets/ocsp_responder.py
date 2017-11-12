# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ocsp_responder.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import socket
import struct
import json
from   PyQt5            import QtCore, QtGui, QtWidgets
import   GenericContainer 
from   TestException    import *


class OcspResponderDialog(object):
    def  __init__(self,container) :
        self.container = container

    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        self.le_name = QtWidgets.QLineEdit(Dialog)
        self.le_name.setObjectName("le_name")
        self.gridLayout.addWidget(self.le_name, 0, 0, 1, 1)

        self.le_ip = QtWidgets.QLineEdit(Dialog)
        self.le_ip.setObjectName("le_port")
        self.gridLayout.addWidget(self.le_ip, 0, 1, 1, 1)

        self.le_port = QtWidgets.QLineEdit(Dialog)
        self.le_port.setObjectName("le_port")
        self.gridLayout.addWidget(self.le_port, 0, 2, 1, 1)


        self.le_delay = QtWidgets.QLineEdit(Dialog)
        self.le_delay.setObjectName("le_delay")
        self.gridLayout.addWidget(self.le_delay, 1, 0, 1, 1)

        self.cb_ocspdir = QtWidgets.QComboBox(Dialog)
        self.cb_ocspdir.setObjectName("cb_ocspdir")
        self.cb_ocspdir.addItem("")
        self.cb_ocspdir.addItem("")
        self.cb_ocspdir.addItem("")
        self.cb_ocspdir.addItem("")
        self.gridLayout.addWidget(self.cb_ocspdir, 1, 1, 1, 2)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        if (self.container.GetType() == GenericContainer.GenericContainer.TYPE_OCSP_OPENSSL_SERVER):
            self.buttonBox.accepted.connect(self.acceptSave)
            obj = self.container.GetBackendObj()
            if  obj :
                self.FillFromObj(obj)
        else :
            self.buttonBox.accepted.connect(self.accept)



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.le_name.setPlaceholderText(_translate("Dialog", "Name"))
        self.le_ip.setPlaceholderText(_translate("Dialog", "IP"))
        self.le_port.setPlaceholderText(_translate("Dialog", "Port"))
        self.le_delay.setPlaceholderText(_translate("Dialog", "Delay"))
        self.cb_ocspdir.setItemText(0, _translate("Dialog", "BANGALORECA"))
        self.cb_ocspdir.setItemText(1, _translate("Dialog", "BHOPALCA"))
        self.cb_ocspdir.setItemText(2, _translate("Dialog", "CALCUTTACA"))
        self.cb_ocspdir.setItemText(3, _translate("Dialog", "DELHICA"))


    def  accept(self) :
        print 'calling accept:'
        try :
            e = self.BuildEntity()
            if not e :
                print 'entity creation failed'
                raise TestException(1)
            if not e.Connect() :
                print 'entity connect failed'
                raise TestException(1)

            e.SendOnce()

        except TestException as e :
            print 'exception in accept:'
            plt = self.le_name.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.le_name.setPalette(plt)
            self.le_name.cursorPositionChanged.connect(self.cursorPositionChanged)
            return

        ew = self.container.AddEntity(e.entity_type)
        ew.SetBackendObj(e)
        self.dialog.accept()



    def acceptSave(self) :
        print 'calling acceptSave:'
        obj = self.container.GetBackendObj()
        obj.delay   = self.le_delay.text()
        obj.cbIndex = self.cb_ocspdir.currentIndex()
        obj.cbName  = self.cb_ocspdir.currentText()

        obj.SendOnce()
        self.dialog.accept()



    def cursorPositionChanged(self,old,new) :
        plt = self.le_name.palette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        self.le_name.setPalette(plt)
        self.le_name.cursorPositionChanged.disconnect()



    def  reject(self) :
        self.dialog.reject()


    def BuildEntity(self) :
        entity = OcspServerEntity(self.le_name.text(),
                                  self.le_ip.text(),
                                  self.le_port.text(),
                                  self.le_delay.text(),
                                  self.cb_ocspdir.currentIndex(),
                                  self.cb_ocspdir.currentText())
                                      
        return entity


    def FillFromObj(self,obj) :
        self.le_name.setText(obj.name)
        self.le_ip.setText(obj.ip)
        self.le_port.setText(obj.port)
        self.le_delay.setText(obj.delay)
        self.cb_ocspdir.setCurrentIndex(obj.cbIndex)






class OcspServerEntity(object) :
    def __init__(self,name,ip,port,delay,cbIndex,cbName) :
        self.name = name
        self.ip = ip
        self.port = port
        self.delay = delay
        self.cbIndex = cbIndex
        self.cbName = cbName
        self.entity_type = GenericContainer.GenericContainer.TYPE_OCSP_OPENSSL_SERVER
        self.sd = None


    def GetType(self) :
        return self.entity_type


    def ToJson(self) :
        d = dict()
        d['name']   = self.name
        d['ip']     = self.ip
        d['port']   =  self.port
        d['delay']  = self.delay
        d['cbIndex']= self.cbIndex
        d['cbName'] = self.cbName
        s = json.dumps(d)
        return s


    def ToFileStr(self) :
        js = self.ToJson()
        d = dict()
        d['type'] = GenericContainer.GenericContainer.TYPE_OCSP_OPENSSL_SERVER
        d['val'] = js
        s = json.dumps(d)
        return s


    @classmethod
    def FromFileStr(cls,jstring) :
        d = json.loads(jstring)
        d = json.loads(d['val'])
        o =  OcspServerEntity(d['name'], d['ip'], d['port'],
                                   d['delay'],d['cbIndex'],
                                   d['cbName'])
        if not o.Connect() :
            o = None

        o.SendOnce()
        return o


    def Connect(self, timeout=2.0) :
        ret = True
        try :
            self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sd.settimeout(timeout)
            self.sd.connect ((self.ip, 2349))

            str = 'twinkletwinkle'
            lstr = struct.pack(">I", len(str))
            self.sd.sendall(lstr)
            self.sd.sendall(str)

            data = self.ReadOnce()
            if not data :
                ret = False
                return ret

            if not data.__eq__('ocspresponder'):
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
        except socket.error as e :
            data = None

        print data                        
        return data


    def  SendOnce(self) :
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


    def IsStartStop(self) :
        return False







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    g = GenericContainer(GenericContainer.CONTAINER_T1)
    ui = OcspResponderDialog(g)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

