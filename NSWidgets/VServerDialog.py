# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ashoke_client.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import socket
import struct
import json
from   PyQt5 import QtCore, QtGui, QtWidgets
from   TestException import *
import GenericContainer
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding


class VServerDialogDialog(object):
    def  __init__(self,container) :
        self.container = container

    def setupUi(self, dialog):
        self.dialog = dialog
        dialog.setObjectName("VServerDialog")
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

        self.lineedit_port = QtWidgets.QLineEdit(dialog)
        self.lineedit_port.setStyleSheet("background-color: rgb(238, 238, 238);")
        self.lineedit_port.setObjectName("lineedit_port")
        self.lineedit_port.setText('')
        self.gridLayout.addWidget(self.lineedit_port, 0, 2, 1, 1)


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
        self.recboundary_comboBox.setItemText(0, _translate("BasicClientDialog", "All One"))
        self.recboundary_comboBox.setItemText(1, _translate("BasicClientDialog", "All Separate"))
        self.recboundary_comboBox.setItemText(2, _translate("BasicClientDialog", "[CKE+CC] [CCV]"))
        self.recboundary_comboBox.setItemText(3, _translate("BasicClientDialog", "[CKE] [CC+CCV]"))
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

            #e.SendOnce()

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
      
        obj.SendOnce()
        self.dialog.accept()
 


    def  reject(self) :
        self.dialog.reject()



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
                                        #int(self.lineedit_port.text()),
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
    


class VServerEntity(object):
    def __init__(self,name,ip,port,type,sess) :
        self.name  = name
        self.ip    = ip
        self.port  = port
        self.type  = type
        self.entity = None
        self.sess = sess


    def Create(self) :
        sslv = lbvserver.lbvserver()
        sslv.name = self.name
        sslv.servicetype = self.type
        sslv.port = self.port
        sslv.ipv46 = self.ip

        self.entity = lbvserver.lbvserver.add(self.sess,l)
        return self,entity


    def Get(self) :
        self.entity = lbvserver.lbvserver.add(self.sess,self.name)      
        return self.entity


    def BindServerCert(self,certname) :
        ret = True
        ckey = sslvserver_sslcertkey_binding.sslvserver_sslcertkey_binding()
	try :
	    ckey.vservername = server 
            ckey.certkeyname = certkey 
            sslvserver_sslcertkey_binding.add(self.sess,ckey)

	except NITROEXCEPTION.nitro_exception as e :
            ret = False

        return ret

  



if __name__ == "__main__":
    import sys
    b = BasicClientEntity('ashoke','10.102.28.1',4040,'certfile','keyfile',
                          'certchainfile','TLS1.2','ECDHE')
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    Form = GenericContainer(GenericContainer.CONTAINER_L1)
    ui = BasicClientDialog(Form)
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

