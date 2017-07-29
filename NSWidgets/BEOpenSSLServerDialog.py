# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BEOpenSSLServerDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import socket
import struct
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from GenericContainer import *
from TestException import *

class BEOpenSSLServerDialog(object):
    def  __init__(self,container) :
        self.container = container
        #self.dialog = QtWidgets.QDialog()
        #self.setupUi(self.dialog)

    
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
        self.lineEdit_4 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_4.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 1, 0, 1, 1)
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
        self.lineEdit_8.setEnabled(False)
        self.lineEdit_8.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout.addWidget(self.lineEdit_8, 2, 1, 1, 1)
        self.lineEdit_9 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_9.setEnabled(False)
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
        #self.buttonBox.accepted.connect(dialog.accept)
        #self.buttonBox.rejected.connect(dialog.reject)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        if (self.container.GetType() == GenericContainer.TYPE_BE_OPENSSL_SERVER) :
            obj = self.container.GetBackendObj()
            if  obj :
                self.FillFromObj(obj)
            


    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "BE OpenSSL Server"))
        self.lineEdit.setPlaceholderText(_translate("dialog", "Name"))
        self.lineEdit_2.setPlaceholderText(_translate("dialog", "IP Address"))
        self.lineEdit_3.setPlaceholderText(_translate("dialog", "Port"))
        self.lineEdit_4.setPlaceholderText(_translate("dialog", "Response Size"))
        self.lineEdit_5.setPlaceholderText(_translate("dialog", "Record size"))
        self.lineEdit_6.setPlaceholderText(_translate("dialog", "Inter Record Delay"))
        self.lineEdit_7.setPlaceholderText(_translate("dialog", "Cipher Filter"))
        self.checkBox.setText(_translate("dialog", "Reuse"))
        self.checkBox_2.setText(_translate("dialog", "Reneg"))
        self.checkBox_3.setText(_translate("dialog", "CAuth"))



    def  accept(self) :
        #print 'accept called'

        try :
            e = self.BuildEntity()
            if not e :
                print 'entity creation failed'
                raise TestException(1)
            if not e.Connect() :
                print 'entity connect failed'
                raise TestException(1)

            e.SendOnce()
            data = e.ReadOnce()
            if data :
                print data
            

        except TestException as e :
            plt = self.lineEdit.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.lineEdit.setPalette(plt)
            self.lineEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
            return


        #e = self.BuildEntity()
        #print 'entity created {}'.format(e)
        ew = self.container.AddEntity(e.entity_type)
        ew.SetBackendObj(e)
        self.dialog.accept()
        

    def  reject(self) :
        #print 'reject called'
        self.dialog.reject()



    def cursorPositionChanged(self,old,new) :
        print 'cursorPositionChanged called'
        plt = self.lineEdit.palette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        self.lineEdit.setPalette(plt)
        self.lineEdit.cursorPositionChanged.disconnect()



    def BuildEntity(self) :
        entity = BEOpenSSLServerEntity(self.lineEdit.text(),
                                       self.lineEdit_2.text(),
                                       self.lineEdit_3.text(),
                                       self.lineEdit_4.text(),
                                       self.lineEdit_5.text(),
                                       self.lineEdit_6.text(),
                                       self.lineEdit_7.text(),
                                       self.checkBox.isChecked(),
                                       self.checkBox_2.isChecked(),
                                       self.checkBox_2.isChecked() )
        return entity


    def FillFromObj(self,obj) :
        self.lineEdit.setText(obj.name)
        self.lineEdit_2.setText(obj.ip)
        self.lineEdit_3.setText(obj.listen_port)
        self.lineEdit_4.setText(obj.resp_size)
        self.lineEdit_5.setText(obj.record_size)
        self.lineEdit_6.setText(obj.inter_record_delay)
        self.lineEdit_7.setText(obj.cipher_filter)

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
class BEOpenSSLServerEntity(object):
    #=====================================================#
    def __init__(self,name,ip,port,resp_size,record_size,delay,cipher_filter,reuse,reneg,cauth) :
        self.name = name
        self.ip = ip
        self.listen_port = port
        self.resp_size = resp_size
        self.record_size = record_size
        self.inter_record_delay = delay
        self.cipher_filter = cipher_filter
        self.reuse = reuse
        self.reneg = reneg
        self.cauth = cauth
        self.entity_type = GenericContainer.TYPE_BE_OPENSSL_SERVER
        self.sd = None
        print 'entity created {}'.format(self)


    #=====================================================#
    def GetType(self) :
        return self.entity_type


    #=====================================================#
    def ToJson(self) :
        d = dict()
        d['listen_port'] =  self.listen_port
        d['resp_size']   = self.resp_size
        d['record_size'] = self.record_size
        d['cipher_filter'] = self.cipher_filter
        d['inter_record_delay '] = self.inter_record_delay 
        d['reuse'] = self.reuse
        d['reneg'] = self.reneg
        d['cauth'] = self.cauth
        
        s = json.dumps(d)
        return s


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

        len = struct.unpack("<I",data)
        if(len[0] == 0) :
            return None

        try :
            data = self.sd.recv(len[0])
        except socket.error as e :
            data = None
                                       
        return data


    #=====================================================#
    def  SendOnce(self) :
        str = self.ToJson()
        lstr = struct.pack(">I", len(str))
        self.sd.sendall(lstr)
        self.sd.sendall(str)


    #=====================================================#
    def Terminate(self) :
        str = ''
        lstr = struct.pack(">I", len(str))
        self.sd.sendall(lstr)
        self.sd.close()
        self.sd = None


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

