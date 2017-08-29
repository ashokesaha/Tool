# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VServerDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import  sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSWidgets')

from   PyQt5 import QtCore, QtGui, QtWidgets
import GenericContainer
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding


class SSLVServerDialog(object):
    def  __init__(self,container = None) :
        self.container = container


    def setupUi(self, dialog):
        self.dialog = dialog
        dialog.setObjectName("VServerDialog")
        dialog.resize(480, 410)

        ##############  Row 1   ####################################
        dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout_2 = QtWidgets.QGridLayout(dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.lineEdit_port = QtWidgets.QLineEdit(dialog)
        self.lineEdit_port.setObjectName("lineEdit_port")
       
        self.lineEdit_ip = QtWidgets.QLineEdit(dialog)
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        
        self.lineEdit_name = QtWidgets.QLineEdit(dialog)
        self.lineEdit_name.setAccessibleName("")
        self.lineEdit_name.setAccessibleDescription("")
        self.lineEdit_name.setText("")
        self.lineEdit_name.setObjectName("lineEdit_name")
        
        self.gridLayout_2.addWidget(self.lineEdit_name, 0,0,1,1)
        self.gridLayout_2.addWidget(self.lineEdit_ip, 0,1,1,1)
        self.gridLayout_2.addWidget(self.lineEdit_port, 0,2,1,1)
        ###############################################################


        ################# Row 2 ######################################
        self.listWidget_server_sni_cert = QtWidgets.QListWidget(dialog)
        self.listWidget_server_sni_cert.setWhatsThis("")
        self.listWidget_server_sni_cert.setObjectName("listWidget_server_sni_cert")
        self.gridLayout_2.addWidget(self.listWidget_server_sni_cert, 1,0,1,1)

        self.listWidget_ca_cert = QtWidgets.QListWidget(dialog)
        self.listWidget_ca_cert.setAccessibleDescription("")
        self.listWidget_ca_cert.setObjectName("listWidget_ca_cert")
        self.gridLayout_2.addWidget(self.listWidget_ca_cert, 1,1,1,1)

        self.listWidget_all_certs = QtWidgets.QListWidget(dialog)
        self.listWidget_all_certs.setObjectName("listWidget_all_certs")
        self.gridLayout_2.addWidget(self.listWidget_all_certs, 1,2,1,1)
        ###############################################################



        ################# Row 3 ######################################
        self.widget = QtWidgets.QWidget(dialog)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.radioButton_reuse = QtWidgets.QRadioButton(self.widget)
        self.radioButton_reuse.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_reuse.setObjectName("Reuse")
        self.gridLayout.addWidget(self.radioButton_reuse, 0, 0, 1, 1)
        
        self.radioButton_sighash = QtWidgets.QRadioButton(self.widget)
        self.radioButton_sighash.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_sighash.setObjectName("SigHash")
        self.gridLayout.addWidget(self.radioButton_sighash, 0, 1, 1, 1)
        
        self.radioButton_2 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 1, 0, 1, 1)
        
        self.radioButton_hsts = QtWidgets.QRadioButton(self.widget)
        self.radioButton_hsts.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_hsts.setObjectName("HSTS")
        self.gridLayout.addWidget(self.radioButton_hsts, 1, 1, 1, 1)
        
        self.radioButton_ssl3 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_ssl3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_ssl3.setObjectName("SSLv3")
        self.gridLayout.addWidget(self.radioButton_ssl3, 2, 0, 1, 1)
        
        self.radioButton_subdom = QtWidgets.QRadioButton(self.widget)
        self.radioButton_subdom.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_subdom.setObjectName("SubDomain")
        self.gridLayout.addWidget(self.radioButton_subdom, 2, 1, 1, 1)
        
        self.radioButton_tls1 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_tls1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_tls1.setObjectName("TLS1.0")
        self.gridLayout.addWidget(self.radioButton_tls1, 3, 0, 1, 1)
        
        self.radioButton_dh = QtWidgets.QRadioButton(self.widget)
        self.radioButton_dh.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_dh.setObjectName("DH")
        self.gridLayout.addWidget(self.radioButton_dh, 3, 1, 1, 1)
        
        self.radioButton_tls11 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_tls11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_tls11.setObjectName("TLS1.1")
        self.gridLayout.addWidget(self.radioButton_tls11, 4, 0, 1, 1)
        
        self.radioButton_ersa = QtWidgets.QRadioButton(self.widget)
        self.radioButton_ersa.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_ersa.setObjectName("eRSA")
        self.gridLayout.addWidget(self.radioButton_ersa, 4, 1, 1, 1)
        
        self.radioButton_tls12 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_tls12.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_tls12.setObjectName("TLS1.2")
        self.gridLayout.addWidget(self.radioButton_tls12, 5, 0, 1, 1)
        
        self.radioButton_sendcn = QtWidgets.QRadioButton(self.widget)
        self.radioButton_sendcn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_sendcn.setObjectName("SendCN")
        self.gridLayout.addWidget(self.radioButton_sendcn, 5, 1, 1, 1)
        
        self.gridLayout_2.addWidget(self.widget, 3,0,1,1)

        
        self.widget_2 = QtWidgets.QWidget(dialog)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.comboBox_cauth = QtWidgets.QComboBox(self.widget_2)
        self.comboBox_cauth.setObjectName("CAuth")
        self.comboBox_cauth.addItem("")
        self.comboBox_cauth.addItem("")
        self.comboBox_cauth.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_cauth, 0, 0, 1, 1)
        
        self.comboBox_push = QtWidgets.QComboBox(self.widget_2)
        self.comboBox_push.setObjectName("comboBox_2")
        self.comboBox_push.addItem("")
        self.comboBox_push.addItem("")
        self.comboBox_push.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_push, 0, 1, 1, 1)
        
        self.lineEdit_dhcount = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_dhcount.setObjectName("lineEdit_dhcount")
        self.gridLayout_3.addWidget(self.lineEdit_dhcount, 1, 0, 1, 1)
        
        self.lineEdit_ersacount = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_ersacount.setObjectName("lineEdit_ersacount")
        self.gridLayout_3.addWidget(self.lineEdit_ersacount, 1, 1, 1, 1)
        
        self.lineEdit_idletimeout = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_idletimeout.setObjectName("lineEdit_idletimeout")
        self.gridLayout_3.addWidget(self.lineEdit_idletimeout, 2, 0, 1, 1)
        
        spacerItem = QtWidgets.QSpacerItem(57, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 76, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 76, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 3,1,1,1)
        
        
        self.listWidget_4 = QtWidgets.QListWidget(dialog)
        self.listWidget_4.setEnabled(False)
        self.listWidget_4.setObjectName("listWidget_4")
        self.gridLayout_2.addWidget(self.listWidget_4, 3,2,1,1)
        ###############################################################




        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 4,0,1,1)

        self.retranslateUi(dialog)
        self.buttonBox.rejected.connect(self.dialog.reject)
        if (self.container.GetType() == GenericContainer.GenericContainer.TYPE_SSL_VSERVER):
            self.buttonBox.accepted.connect(self.acceptSave)
            obj = self.container.GetBackendObj()
            if  obj :
                self.FillFromObj(obj)
        else :
            self.buttonBox.accepted.connect(self.accept)




    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "dialog"))
        
        self.lineEdit_port.setPlaceholderText(_translate("dialog", "Port"))
        self.lineEdit_ip.setPlaceholderText(_translate("dialog", "IP"))
        self.lineEdit_name.setPlaceholderText(_translate("dialog", "Name"))

        self.listWidget_all_certs.setToolTip(_translate("dialog", "All Certs"))
        self.listWidget_ca_cert.setToolTip(_translate("dialog", "Bound CA Certs"))
        self.listWidget_server_sni_cert.setToolTip(_translate("dialog", "Bound Server and SNI Certs"))

        self.radioButton_reuse.setText(_translate("dialog", "Reuse"))
        self.radioButton_sighash.setText(_translate("dialog", "SigHash Chk"))
        self.radioButton_2.setText(_translate("dialog", "----"))
        self.radioButton_hsts.setText(_translate("dialog", "HSTS"))
        self.radioButton_ssl3.setText(_translate("dialog", "SSLv3"))
        self.radioButton_subdom.setText(_translate("dialog", "Subdom"))
        self.radioButton_tls1.setText(_translate("dialog", "TLS1.0"))
        self.radioButton_dh.setText(_translate("dialog", "DH"))
        self.radioButton_tls11.setText(_translate("dialog", "TLS1.1"))
        self.radioButton_ersa.setText(_translate("dialog", "eRSA"))
        self.radioButton_tls12.setText(_translate("dialog", "TLS1.2"))
        self.radioButton_sendcn.setText(_translate("dialog", "Send CN"))

        self.comboBox_cauth.setToolTip(_translate("dialog", "Client Auth"))
        self.comboBox_cauth.setItemText(0, _translate("dialog", "Disabled"))
        self.comboBox_cauth.setItemText(1, _translate("dialog", "Mandatory"))
        self.comboBox_cauth.setItemText(2, _translate("dialog", "Optional"))
        
        self.comboBox_push.setToolTip(_translate("dialog", "Push Flag Opt"))
        self.comboBox_push.setItemText(0, _translate("dialog", "Always"))
        self.comboBox_push.setItemText(1, _translate("dialog", "Ignore"))
        self.comboBox_push.setItemText(2, _translate("dialog", "Merge"))
        self.comboBox_push.setItemText(3, _translate("dialog", "Timer"))
        
        self.lineEdit_dhcount.setPlaceholderText(_translate("dialog", "DH Count"))
        self.lineEdit_ersacount.setPlaceholderText(_translate("dialog", "eRSA count"))
        self.lineEdit_idletimeout.setPlaceholderText(_translate("dialog", "Idle Timeout"))



    def GetSess(self) :
        return self.container.GetSess()
    



    def accept(self) :
        try :
            e = self.BuildEntity()
            if not e :
                print 'entity creation failed'
                raise TestException(1)

            self.UpdateEntity(e)
            ew = self.container.AddEntity(e.entity_type)
            ew.SetBackendObj(e)
            self.dialog.accept()
            return

        except TestException as e :
            plt = self.lineedit_name.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.lineedit_name.setPalette(plt)
            self.lineedit_name.cursorPositionChanged.connect(self.cursorPositionChanged)
            return



    def acceptSave(self) :
        pass




    def BuildEntity(self) :
        name = self.lineEdit_name.text()
        ip   = self.lineEdit_ip.text()
        port = int(self.lineEdit_port.text())
        sess = self.GetSess()

        obj = SSLVServerEntity(name,ip,port,sess);
        obj.Create()
        return obj



    def UpdateEntity(self,obj) :
        if isChecked(self.radioButton_reuse) :
            obj.ssl.sessreuse = 'ENABLED'
        else :
            obj.ssl.sessreuse = 'DISABLED'

        if isChecked(self.radioButton_ssl3) :
            obj.ssl.ssl3 = 'ENABLED'
        else :
            obj.ssl.ssl3 = 'DISABLED'


        if isChecked(self.radioButton_tls1) :
            obj.ssl.tls1 = 'ENABLED'
        else :
            obj.ssl.tls1 = 'DISABLED'

        if isChecked(self.radioButton_tls11) :
            obj.ssl.tls11 = 'ENABLED'
        else :
            obj.ssl.tls11 = 'DISABLED'

        if isChecked(self.radioButton_tls12) :
            obj.ssl.tls12 = 'ENABLED'
        else :
            obj.ssl.tls12 = 'DISABLED'


        if isChecked(self.radioButton_hsts) :
            hsts = 'ENABLED'
            if isChecked(self.radioButton_subdom) :
                subdom = 'YES'

        if isChecked(self.radioButton_sendcn) :
            obj.ssl.sendclosenotify = 'YES'
        else :
            obj.ssl.sendclosenotify = 'NO'
        

        v = self.comboBox_cauth.currentIndex()
        if v > 0 :
            obj.ssl.clientauth = 'ENABLED'
            if v == 1 :
                obj.ssl.clientcert = 'Mandatory'
            elif v == 2 :
                obj.ssl.clientcert = 'Optional'
        else :
            obj.ssl.clientauth = 'DISABLED'


        obj.ssl.pushenctrigger = self.comboBox_push.currentText()

        if isChecked(self.radioButton_dh) :
            obj.ssl.dh = 'ENABLED'
            obj.ssl.dhfile = 'dh_2048'
        else :
            obj.ssl.dh = 'DISABLED'
            obj.ssl.dhfile = None


        sess = self.GetSess()
        sslvserver.sslvserver.update(sess,obj.ssl)
    


class SSLVServerEntity(object):
    def __init__(self,name,ip,port,type,sess) :
        self.name  = name
        self.ip    = ip
        self.port  = port
        self.type  = type
        self.lb    = None
        self.ssl   = None
        self.sess  = sess


    def Create(self) :
        sslv = lbvserver.lbvserver()
        sslv.name = self.name
        sslv.servicetype = self.type
        sslv.port = self.port
        sslv.ipv46 = self.ip

        self.lb  = lbvserver.lbvserver.add(self.sess,sslv)
        if self.lb :
            self.ssl = sslvserver.sslvserver.get(sess,sslv.name)
        if not self.ssl :
            self.lb = None
        return self.ssl


    def Get(self) :
        self.lb = lbvserver.lbvserver.add(self.sess,self.name)
        self.ssl = sslvserver.sslvserver.get(sess,self.name)
        return self.ssl


    def BindServerCert(self,certname) :
        ret = True
        ckey = sslvserver_sslcertkey_binding.sslvserver_sslcertkey_binding()
        try :
            ckey.vservername = server 
            ckey.certkeyname = certkey 
            sslvserver_sslcertkey_binding.add(self.sess,ckey)
            self.ssl = sslvserver.sslvserver.get(sess,self.name)
        except NITROEXCEPTION.nitro_exception as e :
            ret = False

        return ret






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #Form = QtWidgets.QWidget()
    dialog = QtWidgets.QDialog()
    container = GenericContainer.GenericContainer(GenericContainer.GenericContainer.TYPE_SSL_VSERVER)
    ui = SSLVServerDialog(container)
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

