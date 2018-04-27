# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VServerDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import  sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSWidgets')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')


from   PyQt5 import QtCore, QtGui, QtWidgets

import nssrc.com.citrix.netscaler.nitro.resource.config.basic.service as SERVICE
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver as LBVSERVER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver as SSLVSERVER
import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as CERTKEY
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher as CIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslciphersuite as CIPHERSUITE
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcipher_binding as SSLVSRVRCIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslciphersuite_binding as SSLVSRVRCIPHERSUITE
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice as SSLSERVICE
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice_sslcipher_binding as SSLSVCCIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice_sslciphersuite_binding as SSLSVCCIPHERSUITE



import GenericContainer
import CertInstaller
import test_util
import CustomWidget
import json

class SSLServiceDialog(object):
    def  __init__(self,container = None) :
        self.container = container
        self.curDUT = container.GetCurDUT()
        self.pending_calist = []
        self.pending_clientcert = None
        self.pendingcipherlist = []


    def setupUi(self, dialog):
        self.dialog = dialog
        dialog.setObjectName("SSLServiceDialog")
        dialog.resize(600, 410)

        ##############  Row 1   ####################################
        dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout_2 = QtWidgets.QGridLayout(dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.lineEdit_name = QtWidgets.QLineEdit(dialog)
        self.lineEdit_name.setAccessibleName("")
        self.lineEdit_name.setAccessibleDescription("")
        self.lineEdit_name.setText("")
        self.lineEdit_name.setObjectName("lineEdit_name")

        self.lineEdit_ip = QtWidgets.QLineEdit(dialog)
        self.lineEdit_ip.setObjectName("lineEdit_ip")

        self.lineEdit_port = QtWidgets.QLineEdit(dialog)
        self.lineEdit_port.setObjectName("lineEdit_port")

        self.lineEdit_dummyx = QtWidgets.QLineEdit(dialog)
        self.lineEdit_dummyx.setEnabled(False)
        self.lineEdit_dummyx.setObjectName("lineEdit_dummyx")

        
        self.gridLayout_2.addWidget(self.lineEdit_name,   0,0,1,1)
        self.gridLayout_2.addWidget(self.lineEdit_ip,     0,1,1,1)
        self.gridLayout_2.addWidget(self.lineEdit_port,   0,2,1,1)
        self.gridLayout_2.addWidget(self.lineEdit_dummyx, 0,3,1,1)
        ###############################################################


        ################# Row 2 ######################################
        self.listWidget_server_cert = CustomWidget.ListWidgetDD(1,dialog)
        self.listWidget_server_cert.setWhatsThis("")
        self.listWidget_server_cert.setAcceptDrops(True)
        self.listWidget_server_cert.setDragEnabled(True)
        self.listWidget_server_cert.setObjectName("listWidget_server_cert")

        self.listWidget_sni_cert = CustomWidget.ListWidgetDD(0,dialog)
        self.listWidget_sni_cert.setWhatsThis("")
        self.listWidget_sni_cert.setAcceptDrops(True)
        self.listWidget_sni_cert.setDragEnabled(True)
        self.listWidget_sni_cert.setObjectName("listWidget_sni_cert")

        self.listWidget_ca_cert = CustomWidget.ListWidgetDD(0,dialog)
        self.listWidget_ca_cert.setAccessibleDescription("")
        self.listWidget_ca_cert.setAcceptDrops(True)
        self.listWidget_ca_cert.setDragEnabled(True)
        self.listWidget_ca_cert.setObjectName("listWidget_ca_cert")

        self.listWidget_all_certs = QtWidgets.QListWidget(dialog)
        self.listWidget_all_certs.setObjectName("listWidget_all_certs")
        self.listWidget_all_certs.setDragEnabled(True)

        self.listWidget_sni_cert.setEnabled(False)
        self.gridLayout_2.addWidget(self.listWidget_server_cert,     1,0,1,1)
        self.gridLayout_2.addWidget(self.listWidget_sni_cert,        1,3,1,1)
        self.gridLayout_2.addWidget(self.listWidget_ca_cert,         1,1,1,1)
        self.gridLayout_2.addWidget(self.listWidget_all_certs,       1,2,1,1)
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
        self.radioButton_reuse.setAutoExclusive(False)
        self.gridLayout.addWidget(self.radioButton_reuse, 0, 0, 1, 1)
        
        self.radioButton_sighash = QtWidgets.QRadioButton(self.widget)
        self.radioButton_sighash.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_sighash.setObjectName("SigHash")
        self.radioButton_sighash.setAutoExclusive(False)
        self.gridLayout.addWidget(self.radioButton_sighash, 0, 1, 1, 1)
        
        self.radioButton_serverauth = QtWidgets.QRadioButton(self.widget)
        self.radioButton_serverauth.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_serverauth.setObjectName("ServerAuth")
        self.radioButton_serverauth.setAutoExclusive(False)
        self.gridLayout.addWidget(self.radioButton_serverauth, 1, 0, 1, 1)
        
        self.radioButton_hsts = QtWidgets.QRadioButton(self.widget)
        self.radioButton_hsts.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_hsts.setObjectName("HSTS")
        self.radioButton_hsts.setAutoExclusive(False)
        self.radioButton_hsts.setEnabled(False)
        self.gridLayout.addWidget(self.radioButton_hsts, 1, 1, 1, 1)
        
        self.radioButton_ssl3 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_ssl3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_ssl3.setObjectName("SSLv3")
        self.radioButton_ssl3.setAutoExclusive(False)
        self.gridLayout.addWidget(self.radioButton_ssl3, 2, 0, 1, 1)
        
        self.radioButton_subdom = QtWidgets.QRadioButton(self.widget)
        self.radioButton_subdom.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_subdom.setObjectName("SubDomain")
        self.radioButton_subdom.setAutoExclusive(False)
        self.radioButton_subdom.setEnabled(False)
        self.gridLayout.addWidget(self.radioButton_subdom, 2, 1, 1, 1)
        
        self.radioButton_tls1 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_tls1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_tls1.setObjectName("TLS1.0")
        self.radioButton_tls1.setAutoExclusive(False)
        self.gridLayout.addWidget(self.radioButton_tls1, 3, 0, 1, 1)
        
        self.radioButton_dh = QtWidgets.QRadioButton(self.widget)
        self.radioButton_dh.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_dh.setObjectName("DH")
        self.radioButton_dh.setAutoExclusive(False)
        self.radioButton_dh.setEnabled(False)
        self.gridLayout.addWidget(self.radioButton_dh, 3, 1, 1, 1)
        
        self.radioButton_tls11 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_tls11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_tls11.setObjectName("TLS1.1")
        self.radioButton_tls11.setAutoExclusive(False)
        self.gridLayout.addWidget(self.radioButton_tls11, 4, 0, 1, 1)
        
        self.radioButton_ersa = QtWidgets.QRadioButton(self.widget)
        self.radioButton_ersa.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_ersa.setObjectName("eRSA")
        self.radioButton_ersa.setAutoExclusive(False)
        self.radioButton_ersa.setEnabled(False)
        self.gridLayout.addWidget(self.radioButton_ersa, 4, 1, 1, 1)
        
        self.radioButton_tls12 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_tls12.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_tls12.setObjectName("TLS1.2")
        self.radioButton_tls12.setAutoExclusive(False)
        self.gridLayout.addWidget(self.radioButton_tls12, 5, 0, 1, 1)
        
        self.radioButton_sendcn = QtWidgets.QRadioButton(self.widget)
        self.radioButton_sendcn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_sendcn.setObjectName("SendCN")
        self.radioButton_sendcn.setAutoExclusive(False)
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
        self.comboBox_cauth.setEnabled(False)
        self.gridLayout_3.addWidget(self.comboBox_cauth, 0, 1, 1, 1)
        
        self.comboBox_push = QtWidgets.QComboBox(self.widget_2)
        self.comboBox_push.setObjectName("comboBox_2")
        self.comboBox_push.addItem("")
        self.comboBox_push.addItem("")
        self.comboBox_push.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_push, 0, 0, 1, 1)
        
        self.lineEdit_commonname = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_commonname.setObjectName("lineEdit_commonname")
        self.gridLayout_3.addWidget(self.lineEdit_commonname, 1, 0, 1, 1)
        
        self.lineEdit_ersacount = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_ersacount.setObjectName("lineEdit_ersacount")
        self.lineEdit_ersacount.setEnabled(False)
        self.gridLayout_3.addWidget(self.lineEdit_ersacount, 1, 1, 1, 1)
        
        self.lineEdit_maxreq = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_maxreq.setObjectName("lineEdit_maxreq")
        self.gridLayout_3.addWidget(self.lineEdit_maxreq, 2, 0, 1, 1)
        
        self.lineEdit_dhfile = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_dhfile.setObjectName("lineEdit_dhfile")
        self.lineEdit_dhfile.setEnabled(False)
        self.gridLayout_3.addWidget(self.lineEdit_dhfile, 2, 1, 1, 1)

        self.lineEdit_idletimeout = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_idletimeout.setObjectName("lineEdit_idletimeout")
        self.gridLayout_3.addWidget(self.lineEdit_idletimeout, 3, 0, 1, 1)



        spacerItem1 = QtWidgets.QSpacerItem(20, 76, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 76, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 3,1,1,1)
        

        
        #self.listWidget_boundciphers = QtWidgets.QListWidget(dialog)
        self.listWidget_boundciphers = CustomWidget.ListWidgetDD(0,dialog)
        self.listWidget_boundciphers.setObjectName("listWidget_boundciphers")
        self.listWidget_boundciphers.setAcceptDrops(True)
        self.gridLayout_2.addWidget(self.listWidget_boundciphers, 3,2,1,1)

        self.listWidget_allciphers = QtWidgets.QListWidget(dialog)
        self.listWidget_allciphers.setObjectName("listWidget_allciphers")
        self.listWidget_allciphers.setDragEnabled(True)
        self.gridLayout_2.addWidget(self.listWidget_allciphers, 3,3,1,1)
        ###############################################################




        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 4,0,1,1)

        self.retranslateUi(dialog)
        self.buttonBox.rejected.connect(self.dialog.reject)

        self.listWidget_boundciphers.cipherAdded.connect(self.CipherAdded)
        self.listWidget_boundciphers.cipherDeleted.connect(self.CipherDeleted)

        if (self.container.GetType() == GenericContainer.GenericContainer.TYPE_SSL_SERVICE):
            self.buttonBox.accepted.connect(self.acceptSave)
            obj = self.container.GetBackendObj()
            if  obj :
                self.FillFromObj(obj)
        else :
            self.buttonBox.accepted.connect(self.accept)
            self.listWidget_boundciphers.AddCipherToList('ALL')
            self.listWidget_boundciphers.AddCipherToList('DES')
            self.listWidget_boundciphers.AddCipherToList('RC4')
            self.listWidget_boundciphers.AddCipherToList('EXPORT')


        self.FillCerts()
        self.FillCiphers()
        self.FillCipherSuites()


    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "dialog"))
        
        self.lineEdit_port.setPlaceholderText(_translate("dialog", "Port"))
        self.lineEdit_ip.setPlaceholderText(_translate("dialog", "IP"))
        self.lineEdit_name.setPlaceholderText(_translate("dialog", "Name"))

        self.listWidget_all_certs.setToolTip(_translate("dialog", "All Certs"))
        self.listWidget_ca_cert.setToolTip(_translate("dialog", "Bound CA Certs"))
        self.listWidget_server_cert.setToolTip(_translate("dialog", "Bound Client Certs"))
        self.listWidget_sni_cert.setToolTip(_translate("dialog", "Bound SNI Certs"))


        self.radioButton_reuse.setText(_translate("dialog", "Reuse"))
        self.radioButton_sighash.setText(_translate("dialog", "SigHash Chk"))
        self.radioButton_serverauth.setText(_translate("dialog", "ServerAuth"))
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
        
        self.lineEdit_commonname.setPlaceholderText(_translate("dialog", "CommonName"))
        self.lineEdit_ersacount.setPlaceholderText(_translate("dialog", "eRSA count"))
        self.lineEdit_maxreq.setPlaceholderText(_translate("dialog", "Max Req"))
        self.lineEdit_dhfile.setPlaceholderText(_translate("dialog", "DH File"))
        self.lineEdit_idletimeout.setPlaceholderText(_translate("dialog", "Session Timeout"))

        self.listWidget_boundciphers.setToolTip(_translate("dialog", "Bound Ciphers"))
        self.listWidget_allciphers.setToolTip(_translate("dialog", "Cipher List"))

        self.listWidget_ca_cert.certAdded.connect(self.CACertAdded)
        self.listWidget_ca_cert.certDeleted.connect(self.CACertDeleted)
        self.listWidget_server_cert.certAdded.connect(self.ClientCertAdded)
        self.listWidget_server_cert.certDeleted.connect(self.ClientCertDeleted)



    def GetSess(self) :
        return self.curDUT.sess


    def GetCurDUT(self) :
        return self.curDUT
    

    def FillCerts(self) :
        self.curDUT.sess.relogin()
        clist = CertInstaller.CertInstall.ListCertsFromNS(self.curDUT.sess)
        for c in clist :
            QtWidgets.QListWidgetItem(c,self.listWidget_all_certs)


    def FillCiphers(self) :
        self.curDUT.sess.relogin()
        l = CIPHER.sslcipher.get(self.curDUT.sess)
        ll = [x.ciphername for x in l]
        for x in ll :
            QtWidgets.QListWidgetItem(x,self.listWidget_allciphers)
        


    def FillCipherSuites(self) :
        self.curDUT.sess.relogin()
        l = CIPHERSUITE.sslciphersuite.get(self.curDUT.sess)
        ll = [x.ciphername for x in l]
        for x in ll :
            QtWidgets.QListWidgetItem(x,self.listWidget_allciphers)
   


    def FillBoundCiphers(self) :
        obj = self.container.GetBackendObj()
        if not obj :
            return
        sess = obj.sess
        #self.curDUT.sess.relogin()
        
        l = SSLSVCCIPHER.sslservice_sslcipher_binding.get(sess,obj.name)
        ll = [x.ciphername for x in l if (x.ciphername and (len(x.ciphername) > 0))]
        for x in ll :
            self.listWidget_boundciphers.AddToList(x)

        l = SSLSVCCIPHERSUITE.sslservice_sslciphersuite_binding.get(sess,obj.name)
        ll = [x.ciphername for x in l if len(x.ciphername) > 0]
        for x in ll :
            self.listWidget_boundciphers.AddToList(x)


    def CipherAdded(self,s) :
        vname = self.lineEdit_name.text()
        print 'CipherAdded for {} {}'.format(vname,s)
        if not vname or len(vname) == 0 :
            self.pendingcipherlist.append(s)
            return
        obj = self.container.GetBackendObj()
        if not obj :
            self.pendingcipherlist.append(s)
            return

        #self.curDUT.sess.relogin()
        sess = obj.sess
        
        sv = SSLSVCCIPHER.sslservice_sslcipher_binding()
        sv.servicename = vname
        sv.ciphername  = s
        SSLSVCCIPHER.sslservice_sslcipher_binding.add(sess,sv)
        obj.boundciphers.append(s)
    


    def CipherDeleted(self,s) :
        vname = self.lineEdit_name.text()
        if not vname or len(vname) == 0 :
            self.pendingcipherlist.remove(s)
            return
        obj = self.container.GetBackendObj()
        if not obj :
            self.pendingcipherlist.remove(s)
            return

        sess = obj.sess        
        self.curDUT.sess.relogin()
        sv = SSLSVCCIPHER.sslservice_sslcipher_binding()
        sv.servicename = vname
        sv.ciphername  = s
        SSLSVCCIPHER.sslservice_sslcipher_binding.delete(sess,sv)
        try :
            obj.boundciphers.remove(s)
        except ValueError as e :
            pass



    def CACertAdded(self,s) :
        print 'CACertAdded {}'.format(s)
        obj = self.container.GetBackendObj()
        if not obj :
            self.pending_calist.append(s)
            return
        
        sess = obj.sess
        l = [s]
        #test_util.BindUnbindCACert(self.GetCurDUT().sess,self.lineEdit_name.text(),l,isunbind=False,isservice=True)
        test_util.BindUnbindCACert(sess,self.lineEdit_name.text(),l,isunbind=False,isservice=True)
        obj.calist.append(s)
        print 'added cacert {}  to calist'.format(s)
        return


    def CACertDeleted(self,s) :
        print 'CACertDeleted {}'.format(s)
        l = [s]
        #test_util.BindUnbindCACert(self.GetCurDUT().sess,self.lineEdit_name.text(),l,isunbind=True,isservice=True)
        obj = self.container.GetBackendObj()
        if obj :
            obj.calist.remove(s)
        
        sess = obj.sess
        test_util.BindUnbindCACert(sess,self.lineEdit_name.text(),l,isunbind=True,isservice=True)
        return


    def ClientCertAdded(self,s) :
        print 'ServerCertAdded {}'.format(s)
        obj = self.container.GetBackendObj()
        if not obj :
            self.pending_clientcert = s
            return
        l = [s]

        sess = obj.sess
        #test_util.BindUnbindServerCert(self.GetCurDUT().sess,self.lineEdit_name.text(),s,isunbind=False,isservice=True)
        test_util.BindUnbindServerCert(sess,self.lineEdit_name.text(),s,isunbind=False,isservice=True)
        obj.clientcert = s
        return


    def ClientCertDeleted(self,s) :
        if not s or len(s) == 0 :
            return
        
        l = [s]
        #test_util.BindUnbindServerCert(self.GetCurDUT().sess,self.lineEdit_name.text(),s,isunbind=True,isservice=True)
        obj = self.container.GetBackendObj()
        sess = None
        if obj :
            obj.clientcert = None
            sess = obj.sess
        if not sess :
            return
        test_util.BindUnbindServerCert(sess,self.lineEdit_name.text(),s,isunbind=True,isservice=True)
        return





    def accept(self) :
       
        try :
            obj = self.container.GetBackendObj()
            if obj :
                sess = obj.sess
            else :
                sess = self.curDUT.sess
            
            e = self.BuildEntity()
            if not e :
                print 'entity creation failed'
                return

            if not self.UpdateEntity(e) :
                print 'accept failure (update failed)'
                e.Delete()
                return
            
            ew = self.container.AddEntity(e.entity_type)
            ew.SetBackendObj(e)
            self.dialog.accept()
            return

        except NITROEXCEPTION as e :
            print 'SSLServiceDialog:accept Nitro exception'
            plt = self.lineedit_name.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.lineedit_name.setPalette(plt)
            self.lineedit_name.cursorPositionChanged.connect(self.cursorPositionChanged)
            return
        except Exception as e :
            #raise e
            print 'SSLServiceDialog:accept exception'
            print 'Vserver creation failed: {}'.format(e.message)
            return



    def acceptSave(self) :
        #self.curDUT.sess.relogin()
        obj = self.container.GetBackendObj()
        self.UpdateEntity(obj)
        obj.ToJson()
        self.dialog.accept()



    def BuildEntity(self) :
        try :
            name = self.lineEdit_name.text()
            ip   = self.lineEdit_ip.text()
            port = int(self.lineEdit_port.text())
            sess = self.curDUT.sess
            nsip = self.curDUT.nsip

            obj = SSLServiceEntity(name,ip,port,'SSL',sess,nsip)
            if not obj.Create() :
                print 'Failed to add LB Vserver'
                obj = None
        except Exception as e :
            print 'SSLServiceDialog:BuildEntity exception {}'.format(e.message)
            ob = None

        return obj



    def GetDUTByIP(self,nsip) :
        return self.container.GetDUTByIP(nsip)



    def FillFromDict(self,d, nsip) :
        #dut = self.GetCurDUT()
        #dut = d['dut']
        dut = self.GetDUTByIP(nsip)
        
        
        self.lineEdit_name.setText(d['name'])
        self.lineEdit_ip.setText(d['ip'])
        self.lineEdit_port.setText(str(d['port']))

        if d['sessreuse'] == 'ENABLED' :
            self.radioButton_reuse.setChecked(True)
            self.lineEdit_idletimeout.setText(d['sesstimeout'])
        else :
            self.radioButton_reuse.setChecked(False)
            self.lineEdit_idletimeout.setText('')


        if d['ssl3'] == 'ENABLED' :
            self.radioButton_ssl3.setChecked(True)
        else :
            self.radioButton_ssl3.setChecked(False)

        if d['tls1'] == 'ENABLED' :
            self.radioButton_tls1.setChecked(True)
        else :
            self.radioButton_tls1.setChecked(False)

        if d['tls11'] == 'ENABLED' :
            self.radioButton_tls11.setChecked(True)
        else :
            self.radioButton_tls11.setChecked(False)

        if d['tls12'] == 'ENABLED' :
            self.radioButton_tls12.setChecked(True)
        else :
            self.radioButton_tls12.setChecked(False)


        if d['sendclosenotify'] == 'YES' :
            self.radioButton_sendcn.setChecked(True)
        else :
            self.radioButton_sendcn.setChecked(False)


        if d['serverauth'] == 'ENABLED' :
            self.radioButton_serverauth.setChecked(True)
            self.lineEdit_commonname.setText(str(d['commonname']))
        else :
            self.radioButton_serverauth.setChecked(False)
            self.lineEdit_commonname.setText('')



        v = d['pushenctrigger']
        if v == 'Always' :
            self.comboBox_push.setCurrentIndex(0)
        elif v == 'Ignore' :
            self.comboBox_push.setCurrentIndex(1)
        elif v == 'Merge' :
            self.comboBox_push.setCurrentIndex(2)
        elif v == 'Timer' :
            self.comboBox_push.setCurrentIndex(3)


        self.FillCerts()
        
        clist = d['calist']
        if len(clist) > 0 :
            test_util.BindUnbindCACert(dut.sess,d['name'],clist,isunbind=False,isservice=True)
            for c in clist :
                self.listWidget_ca_cert.AddToList(c)

        clist = d['clientcert']
        if clist :
            test_util.BindUnbindServerCert(dut.sess,d['name'], clist,isunbind=False,isservice=True)
            self.listWidget_server_cert.AddToList(clist)





    def FillFromObj(self,obj) :
        print 'service FillFromObj called. fromfiledict {}'.format(obj.fromfiledict)
        if obj.fromfiledict :
            # The case when we are coming from Load. In this case
            # We shall have the LB Vserver details in obj and SSL details
            # in the dict.  After loading we create the widget without
            # creating the vserver. User needs to go to <properties> .
            # We shall call this function at that time and we shall be
            # creating the LB Vserver part here (while opening up the
            # property dialog).
            # Once user chooses <ok>, we shall call acceptSave() and then
            # we shall call UpdateEntity() to update SSL properties
            
            self.FillFromDict(obj.fromfiledict, obj.nsip)
            obj.fromfiledict = None
            self.FillBoundCiphers()
            return
        
        self.lineEdit_name.setText(obj.name)
        self.lineEdit_ip.setText(obj.ip)
        self.lineEdit_port.setText(str(obj.port))

        
        if obj.sslsvc.sessreuse == 'ENABLED' :
            self.radioButton_reuse.setChecked(True)
            self.lineEdit_idletimeout.setText(str(obj.sslsvc.sesstimeout))
        else :
            self.radioButton_reuse.setChecked(False)
            self.lineEdit_idletimeout.setText('')

        if obj.sslsvc.serverauth == 'ENABLED' :
            self.radioButton_serverauth.setChecked(True)
            self.lineEdit_commonname.setText(str(obj.sslsvc.commonname))
        else :
            self.radioButton_serverauth.setChecked(False)
            self.lineEdit_commonname.setText('')


        if obj.sslsvc.ssl3 == 'ENABLED' :
            self.radioButton_ssl3.setChecked(True)
        else :
            self.radioButton_ssl3.setChecked(False)

        if obj.sslsvc.tls1 == 'ENABLED' :
            self.radioButton_tls1.setChecked(True)
        else :
            self.radioButton_tls1.setChecked(False)

        if obj.sslsvc.tls11 == 'ENABLED' :
            self.radioButton_tls11.setChecked(True)
        else :
            self.radioButton_tls11.setChecked(False)

        if obj.sslsvc.tls12 == 'ENABLED' :
            self.radioButton_tls12.setChecked(True)
        else :
            self.radioButton_tls12.setChecked(False)


        if obj.sslsvc.sendclosenotify == 'YES' :
            self.radioButton_sendcn.setChecked(True)
        else :
            self.radioButton_sendcn.setChecked(False)


        if obj.sslsvc.strictsigdigestcheck == 'ENABLED' :
            self.radioButton_sighash.setChecked(True)
        else :
            self.radioButton_sighash.setChecked(False)

        clist = obj.calist
        for c in clist :
            self.listWidget_ca_cert.AddToList(c)

        clist = obj.clientcert
        if clist :
            self.listWidget_server_cert.AddToList(clist)

        self.FillBoundCiphers()

      

    def UpdateEntity(self,obj) :
        ret = True
        clientcertlist = []
        cacertlist   = []
        dut = self.GetCurDUT()

        
        svcname = self.lineEdit_name.text()
        
        cslist = []
        if self.pendingcipherlist :
            print 'UpdateEntity: svcname {}'.format(svcname)
            test_util.BindUnbindCipher(dut.sess,svcname,self.pendingcipherlist, cslist,isunbind=False,isservice=True)
            obj.boundciphers =  self.pendingcipherlist
            self.pendingcipherlist = None
        
        if self.pending_calist :
            test_util.BindUnbindCACert(dut.sess,svcname, self.pending_calist,isunbind=False,isservice=True)
            obj.calist =  self.pending_calist
            self.pending_calist = None

        if self.pending_clientcert :
            test_util.BindUnbindServerCert(dut.sess,svcname, self.pending_clientcert,isunbind=False,isservice=True)
            obj.clientcert =  self.pending_clientcert
            self.pending_clientcert = None


        if self.radioButton_reuse.isChecked() :
            obj.sslsvc.sessreuse = 'ENABLED'
            try :
                obj.sslsvc.sesstimeout = int(self.lineEdit_idletimeout.text())
            except ValueError as e :
                obj.sslsvc.sesstimeout = 120
                self.lineEdit_idletimeout.setText('120')
        else :
            obj.sslsvc.sessreuse = 'DISABLED'
            obj.sslsvc.sesstimeout = None
            self.lineEdit_idletimeout.setText('')



        if self.radioButton_ssl3.isChecked() :
            obj.sslsvc.ssl3 = 'ENABLED'
        else :
            obj.sslsvc.ssl3 = 'DISABLED'

        if self.radioButton_tls1.isChecked() :
            obj.sslsvc.tls1 = 'ENABLED'
        else :
            obj.sslsvc.tls1 = 'DISABLED'

        if self.radioButton_tls11.isChecked() :
            obj.sslsvc.tls11 = 'ENABLED'
        else :
            obj.sslsvc.tls11 = 'DISABLED'

        if self.radioButton_tls12.isChecked() :
            obj.sslsvc.tls12 = 'ENABLED'
        else :
            obj.sslsvc.tls12 = 'DISABLED'


        if self.radioButton_sendcn.isChecked() :
            obj.sslsvc.sendclosenotify = 'YES'
        else :
            obj.sslsvc.sendclosenotify = 'NO'

  
        if self.radioButton_sighash.isChecked() :
            obj.sslsvc.strictsigdigestcheck = 'ENABLED'
        else :
            obj.sslsvc.strictsigdigestcheck = 'DISABLED'

       
        if self.radioButton_ersa.isChecked() :
            obj.sslsvc.ersa = 'ENABLED'
            try :
                ersacount = int(self.lineEdit_ersacount.text())
            except ValueError as e :
                obj.sslsvc.ersa = 'DISABLED'
                ersacount = None
            
            obj.sslsvc.ersacount = ersacount
            self.lineEdit_ersacount.setText(str(ersacount))
        else :
            obj.sslsvc.ersa = 'DISABLED'
            obj.sslsvc.ersacount = None


        if self.radioButton_serverauth.isChecked() :
            obj.sslsvc.serverauth = 'ENABLED'
            obj.sslsvc.commonname = self.lineEdit_commonname.text()
        else :
            obj.sslsvc.serverauth = 'DISABLED'
            obj.sslsvc.commonname = None




        obj.sslsvc.dhfile = None
        obj.sslsvc.cipherurl = None
        obj.sslsvc.sslv2url = None
        obj.sslsvc.dtlsprofilename = None
        obj.sslsvc.sslprofile = None
        obj.sslsvc.pushenctrigger = None
        

        t = self.lineEdit_maxreq.text()
        if t and len(t) > 0 :
            obj.svc.maxreq = int(t)
            
        obj.svc.cipheader = None
        obj.svc.sc = None
        obj.svc.serverid = None
        obj.svc.weight = None
        obj.svc.monitor_name_svc = None
        obj.svc.tcpprofilename = None
        obj.svc.httpprofilename = None
        obj.svc.netprofile     = None
        obj.svc.dnsprofilename     = None
        obj.svc.hashid     = None
        obj.svc.comment     = None
        obj.sslsvc.clientcert = None

        sess = self.curDUT.sess
        try :
            SERVICE.service.update(sess,obj.svc)
            SSLSERVICE.sslservice.update(sess,obj.sslsvc)
        except NITROEXCEPTION as e :
            print 'UpdateEntity Nitro service failed : {}'.format(e.message)
            ret = False
            raise e
        except Exception as e :
            print 'UpdateEntity service failed : {}'.format(e.message)
            ret = False
            raise e

        return ret




class SSLServiceEntity(QtCore.QObject):
    sigStatus = QtCore.pyqtSignal(int)
    def __init__(self,name,ip,port,vtype,sess,nsip=None) :
        super(self.__class__,self).__init__()
        self.name       = name
        self.ip         = ip
        self.port       = port
        self.type       = vtype
        self.svc        = None
        self.sslsvc     = None
        self.sess       = sess
        self.nsip       = nsip
        self.boundciphers = None
        self.fromfiledict = None
        self.isrunning = False
        self.calist = []
        self.clientcert = None
        self.boundciphers = []

        self.entity_type = GenericContainer.GenericContainer.TYPE_SSL_SERVICE



    def GetName(self) :
        name = self.name + '\n' + self.ip + '\n' + str(self.port)
        return name


    def UpDownSlot(self, i) :
        if i > 0 :
            self.isRunning = True
        else :
            self.isRunning = False
        

    def Create(self) :
        print 'service create called'
        sslsvc = SERVICE.service()
        sslsvc.name = self.name
        sslsvc.servicetype = self.type
        sslsvc.port = self.port
        sslsvc.ip = self.ip

        try :
            self.svc  = SERVICE.service.add(self.sess,sslsvc)
            if self.svc :
                test_util.BindMonitor(self.sess,sslsvc.name,'quick_mon')
                self.svc    = SERVICE.service.get(self.sess,sslsvc.name)
                self.sslsvc = SSLSERVICE.sslservice.get(self.sess,sslsvc.name)
            if not self.sslsvc :
                self.svc = None
        except NITROEXCEPTION as e :
            print 'SSLServiceEntity:Create: NitroException{}'.format(e.message)
            self.svc = None
            self.sslsvc = None
            print '{}'.format(e.message)
        except Exception as e :
            print 'SSLServiceEntity:Create: Exception{}'.format(e.message)
            self.svc = None
            self.sslsvc = None

        self.boundciphers.append('DEFAULT_BACKEND')
        return self.sslsvc



    def Refresh(self) :
        try :
            if self.svc :
                self.svc  = SERVICE.service.get(self.sess,self.svc.name)
        except NITROEXCEPTION as e :
            print 'SSLServiceEntity:Refresh: NitroException{}'.format(e.message)
            self.svc = None
            self.sslsvc = None
            print '{}'.format(e.message)
        except Exception as e :
            print 'SSLServiceEntity:Refresh: Exception{}'.format(e.message)
            self.svc = None
            self.sslsvc = None

        if self.svc :
            if self.svc.svrstate == 'UP' :
                self.isrunning = True
            else :
                self.isrunning = False



    def Delete(self) :
        sslv = SERVICE.service()
        sslv.name = self.name
        sslv.servicetype = self.type
        sslv.port = self.port
        sslv.ip = self.ip

        self.sess.relogin()
        try :
            SERVICE.service.delete(self.sess,sslv)
        except NITROEXCEPTION as e :
            self.lb = None
            self.ssl = None
            print '{}'.format(e.message)
        except Exception as e :
            self.lb = None
            self.ssl = None
            print '{}'.format(e.message)
            


    def IsRunning(self) :
        return self.isrunning

    def IsStartStop(self) :
        return False

    def IsResults(self) :
        return False

    def IsProperty(self) :
        return True

    def Start(self) :
        return
    
    def GetType(self) :
        return self.entity_type


    def ToJson(self) :
        print 'ToJson: calist {}'.format(self.calist)
        d = dict()
        d['name'] = self.name
        d['ip'] = self.ip
        d['nsip'] = self.nsip
        d['port']  = self.port
        d['type']  = self.type
        d['calist'] = self.calist
        d['clientcert'] = self.clientcert
        d['sessreuse'] = self.sslsvc.sessreuse
        d['sesstimeout'] = self.sslsvc.sesstimeout
        d['ssl3']   = self.sslsvc.ssl3
        d['tls1']   = self.sslsvc.tls1
        d['tls11'] = self.sslsvc.tls11
        d['tls12'] = self.sslsvc.tls12
        d['sendclosenotify']       = self.sslsvc.sendclosenotify
        d['serverauth'] = self.sslsvc.serverauth
        d['boundciphers'] = self.boundciphers

        if (hasattr(self.sslsvc,'pushenctrigger')) :
            d['pushenctrigger'] = self.sslsvc.pushenctrigger
        else :
            d['pushenctrigger'] = None

        if (hasattr(self.sslsvc,'commonname')) :
            d['commonname'] = self.sslsvc.commonname
        else :
            d['commonname'] = None

        
        s = json.dumps(d)
        return s



    def ToFileStr(self) :
        js = self.ToJson()
        d = dict()
        d['type'] = self.entity_type
        d['val'] = js
        s = json.dumps(d)
        return s


    def AllowDrop(self,jstring) :
        return False


    def PrepareMimeData(self, ccode=None) :
        d = dict()
        d['type'] = self.entity_type
        d['name'] = self.name
        # Dont want service to chnage color of the widget where it is dropped
        d['ccode'] = None
        s = json.dumps(d)
        return s


    def HandleDropEvent(self,jsonStr) :
        return



    def ApplySavedCiphers(self,sess=None) :
        ll = SSLSVCCIPHERSUITE.sslservice_sslciphersuite_binding.get(sess,self.name)
        ll = [l.ciphername for l in ll]
        set_ll = set(ll)
        set_bound = set(self.boundciphers)

        l = set_ll - set_bound
        svlist = []
        print set_ll
        print set_bound
        print l
        for x in l :
            sv = SSLSVCCIPHERSUITE.sslservice_sslciphersuite_binding()
            sv.servicename = self.name
            sv.ciphername = str(x)
            svlist.append(sv)
            SSLSVCCIPHERSUITE.sslservice_sslciphersuite_binding.delete(sess,sv)

        l = set_bound - set_ll
        svlist = []
        for x in l :
            sv = SSLSVCCIPHERSUITE.sslservice_sslciphersuite_binding()
            sv.servicename = self.name
            sv.ciphername = str(x)
            svlist.append(sv)
            SSLSVCCIPHERSUITE.sslservice_sslciphersuite_binding.add(sess,sv)



    def GetDUTByIP(self,nsip) :
        return self.parent.GetDUTByIP(nsip)




    @classmethod
    def FromFileStr(cls,jstring,sess=None) :
        d = json.loads(jstring)
        d = json.loads(d['val'])

        try :
            svc = SERVICE.service.get(sess,d['name'])
            if(svc) :
                print 'deleting existing service {}'.format(d['name'])
                SERVICE.service.delete(sess,svc)
        except NITROEXCEPTION as e :
            print 'FromFileStr: nitro exception: {}'.format(e.message)
        except Exception as e :
            print 'FromFileStr: exception: {}'.format(e.message)
        

        obj = SSLServiceEntity(d['name'],d['ip'],d['port'],d['type'],sess,d['nsip'])
        obj.fromfiledict = d
        obj.sess = sess
    
        if not obj.Create() :
            print 'obj.Create() failed'
            return None

        l = d['calist']
        if len(l) > 0 :
            print 'binding ca cert {}'.format(l)
            test_util.BindUnbindCACert(sess,d['name'],l,isunbind=False,isservice=True)

        l = d['clientcert']
        if l :
            print 'binding client cert {}'.format(l)
            test_util.BindUnbindServerCert(sess,d['name'],l,isunbind=False,isservice=True)


        obj.sslsvc.sessreuse = d['sessreuse']
        obj.sslsvc.sesstimeout = d['sesstimeout'] 
        obj.sslsvc.ssl3  = d['ssl3']
        obj.sslsvc.tls1   = d['tls1']
        obj.sslsvc.tls11 = d['tls11']
        obj.sslsvc.tls12 = d['tls12']
        obj.sslsvc.sendclosenotify = d['sendclosenotify']
        obj.sslsvc.clientcert = d['clientcert'] 
        obj.sslsvc.pushenctrigger = d['pushenctrigger']
        obj.sslsvc.serverauth = d['serverauth']
        obj.sslsvc.commonname = d['commonname']
        obj.boundciphers = d['boundciphers']
        
        obj.ApplySavedCiphers(sess)
        return obj







##if __name__ == "__main__":
##    sess = test_util.Login('10.102.28.201')
##    
##    lbv = LBVSERVER.lbvserver()
##    lbv.name = 'one'
##    lbv.servicetype = 'SSL'
##    lbv.port = 5557
##    lbv.ipv46 = '10.102.28.20'
##
##    lb  = LBVSERVER.lbvserver.add(sess,lbv)
##    
##    sslv = SSLVSERVER.sslvserver.get(sess,lbv.name)
##    sslv.tls12 = 'DISABLED'
##    sslv.dhfile = None
##    sslv.cipherurl = None
##    sslv.sslv2url = None
##    sslv.clientcert = None
##    sslv.dtlsprofilename = None
##    sslv.sslprofile = None
##    sslv.sessreuse = 'DISABLED'
##    sslv.sesstimeout = None
##    
##    SSLVSERVER.sslvserver.update(sess,sslv)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    container = GenericContainer.GenericContainer(GenericContainer.GenericContainer.TYPE_SSL_VSERVER)
    ui = SSLServiceDialog(container)
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

