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

import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver as LBVSERVER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver as SSLVSERVER
import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as CERTKEY
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher as CIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslciphersuite as CIPHERSUITE
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcipher_binding as SSLVSRVRCIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslciphersuite_binding as SSLVSRVRCIPHERSUITE
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding as LBVSRVRSVC



import GenericContainer
import CertInstaller
import test_util
import CustomWidget
import json

class SSLVServerDialog(object):
    def  __init__(self,container = None) :
        self.container = container
        self.curDUT = container.GetCurDUT()


    def setupUi(self, dialog):
        self.dialog = dialog
        dialog.setObjectName("VServerDialog")
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

        self.gridLayout_2.addWidget(self.listWidget_server_cert,     1,0,1,1)
        self.gridLayout_2.addWidget(self.listWidget_sni_cert,        1,1,1,1)
        self.gridLayout_2.addWidget(self.listWidget_ca_cert,         1,2,1,1)
        self.gridLayout_2.addWidget(self.listWidget_all_certs,       1,3,1,1)
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
        
        self.radioButton_sni = QtWidgets.QRadioButton(self.widget)
        self.radioButton_sni.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_sni.setObjectName("radioButton_sni")
        self.radioButton_sni.setAutoExclusive(False)
        self.gridLayout.addWidget(self.radioButton_sni, 1, 0, 1, 1)
        
        self.radioButton_hsts = QtWidgets.QRadioButton(self.widget)
        self.radioButton_hsts.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_hsts.setObjectName("HSTS")
        self.radioButton_hsts.setAutoExclusive(False)
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
        
        self.lineEdit_dhfile = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_dhfile.setObjectName("lineEdit_dhfile")
        self.gridLayout_3.addWidget(self.lineEdit_dhfile, 2, 1, 1, 1)


        spacerItem1 = QtWidgets.QSpacerItem(20, 76, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 76, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 3,1,1,1)
        

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
        
        if (self.container.GetType() == GenericContainer.GenericContainer.TYPE_SSL_VSERVER):
            self.buttonBox.accepted.connect(self.acceptSave)
            obj = self.container.GetBackendObj()
            if  obj :
                self.curDUT = self.GetDUTByIP(obj.nsip)
                self.FillFromObj(obj)
        else :
            self.buttonBox.accepted.connect(self.accept)

        self.FillCerts()
        self.FillCiphers()
        self.FillCipherSuites()

        self.listWidget_boundciphers.cipherAdded.connect(self.CipherAdded)
        self.listWidget_boundciphers.cipherDeleted.connect(self.CipherDeleted)

        self.listWidget_ca_cert.certAdded.connect(self.CACertAdded)
        self.listWidget_ca_cert.certDeleted.connect(self.CACertDeleted)
        self.listWidget_sni_cert.certAdded.connect(self.SNICertAdded)
        self.listWidget_sni_cert.certDeleted.connect(self.SNICertDeleted)
        self.listWidget_server_cert.certAdded.connect(self.ServerCertAdded)
        self.listWidget_server_cert.certDeleted.connect(self.ServerCertDeleted)


    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "dialog"))
        
        self.lineEdit_port.setPlaceholderText(_translate("dialog", "Port"))
        self.lineEdit_ip.setPlaceholderText(_translate("dialog", "IP"))
        self.lineEdit_name.setPlaceholderText(_translate("dialog", "Name"))

        self.listWidget_all_certs.setToolTip(_translate("dialog", "All Certs"))
        self.listWidget_ca_cert.setToolTip(_translate("dialog", "Bound CA Certs"))
        self.listWidget_server_cert.setToolTip(_translate("dialog", "Bound Server Certs"))
        self.listWidget_sni_cert.setToolTip(_translate("dialog", "Bound SNI Certs"))


        self.radioButton_reuse.setText(_translate("dialog", "Reuse"))
        self.radioButton_sighash.setText(_translate("dialog", "SigHash Chk"))
        self.radioButton_sni.setText(_translate("dialog", "SNI"))
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
        self.lineEdit_dhfile.setPlaceholderText(_translate("dialog", "DH File"))

        self.listWidget_boundciphers.setToolTip(_translate("dialog", "Bound Ciphers"))
        self.listWidget_allciphers.setToolTip(_translate("dialog", "Cipher List"))



    def GetSess(self) :
        return self.curDUT.sess


    def GetCurDUT(self) :
        return self.curDUT
    


    def FillCerts(self) :
        for c in  self.curDUT.allcerts :
            QtWidgets.QListWidgetItem(c,self.listWidget_all_certs)


    def FillCiphers(self) :
        l = self.curDUT.allciphers
        ll = [x.ciphername for x in l]
        for x in ll :
            QtWidgets.QListWidgetItem(x,self.listWidget_allciphers)


    def FillCipherSuites(self) :
        l = self.curDUT.allciphersuites
        ll = [x.ciphername for x in l]
        for x in ll :
            QtWidgets.QListWidgetItem(x,self.listWidget_allciphers)




    def FillBoundCiphers(self) :
        obj = self.container.GetBackendObj()
        if not obj :
            return
        for x in obj.boundciphers :
            self.listWidget_boundciphers.AddToList(x)



    def CipherAdded(self,s) :
        vname = self.lineEdit_name.text()
        if not vname or len(vname) == 0 :
            return
        obj = self.container.GetBackendObj()
        if not obj :
            return
        
        self.curDUT.sess.relogin()
        sv = SSLVSRVRCIPHER.sslvserver_sslcipher_binding()
        sv.vservername = vname
        sv.ciphername  = s
        SSLVSRVRCIPHER.sslvserver_sslcipher_binding.add(self.curDUT.sess,sv)
        obj.boundciphers.append(s)


    def CipherDeleted(self,s) :
        vname = self.lineEdit_name.text()
        if not vname or len(vname) == 0 :
            return
        obj = self.container.GetBackendObj()
        if not obj :
            return

        self.curDUT.sess.relogin()
        sv = SSLVSRVRCIPHER.sslvserver_sslcipher_binding()
        sv.vservername = vname
        sv.ciphername  = s
        SSLVSRVRCIPHER.sslvserver_sslcipher_binding.delete(self.curDUT.sess,sv)
        try :
            obj.boundciphers.remove(s)
        except ValueError as e :
            pass
 

    def CACertAdded(self,s) :
        l = [s]
        test_util.BindUnbindCACert(self.GetCurDUT().sess,self.lineEdit_name.text(),l,isunbind=False)
        return

    def CACertDeleted(self,s) :
        l = [s]
        test_util.BindUnbindCACert(self.GetCurDUT().sess,self.lineEdit_name.text(),l,isunbind=True)
        return

    def SNICertAdded(self,s) :
        l = [s]
        test_util.BindUnbindSniCert(self.GetCurDUT().sess,self.lineEdit_name.text(),l,isunbind=False)
        return

    def SNICertDeleted(self,s) :
        l = [s]
        test_util.BindUnbindSniCert(self.GetCurDUT().sess,self.lineEdit_name.text(),l,isunbind=True)
        return

    def ServerCertAdded(self,s) :
        l = [s]
        test_util.BindUnbindServerCert(self.GetCurDUT().sess,self.lineEdit_name.text(),s,isunbind=False)
        return

    def ServerCertDeleted(self,s) :
        l = [s]
        test_util.BindUnbindServerCert(self.GetCurDUT().sess,self.lineEdit_name.text(),s,isunbind=True)
        return




    def FormSanity(self) :
        try :
            ersacount = int(self.lineEdit_ersacount.text())
        except ValueError as e :
            ersacount = 0

        try :
            dhcount   = int(self.lineEdit_dhcount.text())
        except ValueError as e :
            dhcount = 0


        if (ersacount and (ersacount < 512)) :
            print 'Error : Bad ersacount .. '
            return False

        if (dhcount and (dhcount < 512)) :
            print 'Error : Bad dhcount .. '
            return False

        return True




    def accept(self) :
        if not self.FormSanity() :
            return
        
        try :
            self.curDUT.sess.relogin()
            e = self.BuildEntity()
            if not e :
                print 'entity creation failed'
                return

            self.curDUT.sess.relogin()
            if not self.UpdateEntity(e) :
                print 'accept failure (update failed)'
                e.Delete()
                return
            
            ew = self.container.AddEntity(e.entity_type)
            ew.SetBackendObj(e)
            self.dialog.accept()
            return

        except NITROEXCEPTION as e :
            plt = self.lineedit_name.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.lineedit_name.setPalette(plt)
            self.lineedit_name.cursorPositionChanged.connect(self.cursorPositionChanged)
            return
        except Exception as e :
            print 'Vserver creation failed: {}'.format(e.message)
            return



    def acceptSave(self) :
        if not self.FormSanity() :
            return

        self.curDUT.sess.relogin()
        obj = self.container.GetBackendObj()
        self.UpdateEntity(obj)
        obj.ToJson()
        self.dialog.accept()



    def GetDUTByIP(self,nsip) :
        return self.container.GetDUTByIP(nsip)



    def BuildEntity(self) :
        name = self.lineEdit_name.text()
        ip   = self.lineEdit_ip.text()
        port = int(self.lineEdit_port.text())
        sess = self.curDUT.sess

        dut = self.GetCurDUT()
        obj = SSLVServerEntity(name,ip,port,'SSL',sess, dut.nsip);
        if not obj.Create() :
            print 'Failed to add LB Vserver'
            return None
        
        return obj




    def FillFromDict(self,d) :
        print 'FillFromDict : calist {} '.format(d['calist'])
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

        if d['snienable'] == 'ENABLED' :
            self.radioButton_sni.setChecked(True)
        else :
            self.radioButton_sni.setChecked(False)


        if d['clientauth'] == 'DISABLED' :
            curidx = 0
        else :
            if d['clientcert'] == 'Mandatory' :
                curidx = 1
            else :
                curidx = 2
        self.comboBox_cauth.setCurrentIndex(curidx)


        v = d['pushenctrigger']
        if v == 'Always' :
            self.comboBox_push.setCurrentIndex(0)
        elif v == 'Ignore' :
            self.comboBox_push.setCurrentIndex(1)
        elif v == 'Merge' :
            self.comboBox_push.setCurrentIndex(2)
        elif v == 'Timer' :
            self.comboBox_push.setCurrentIndex(3)


        if d['dh'] == 'ENABLED' :
            self.lineEdit_dhfile.setText(d['dhfile'])
            self.lineEdit_dhcount.setText(str(d['dhcount']))
            self.radioButton_dh.setChecked(True)
        else :
            self.lineEdit_dhfile.setText('')
            self.lineEdit_dhcount.setText('')
            self.radioButton_dh.setChecked(False)


        if d['ersa'] == 'ENABLED' :
            self.lineEdit_ersacount.setText(str(d['ersacount']))
            self.radioButton_ersa.setChecked(True)
        else :
            self.lineEdit_ersacount.setText('')
            self.radioButton_ersa.setChecked(False)


        self.FillCerts()
        clist = d['calist']
        for c in clist :
            self.listWidget_ca_cert.AddToList(c)

        clist = d['snilist']
        for c in clist :
            self.listWidget_sni_cert.AddToList(c)

        clist = d['servercert']
        self.listWidget_server_cert.AddToList(clist)
        self.ServerCertAdded(clist)




    def FillFromObj(self,obj) :
        print 'FillFromObj : '
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
            
            self.FillFromDict(obj.fromfiledict)
            obj.fromfiledict = None
            self.FillBoundCiphers()
            return
        
        self.lineEdit_name.setText(obj.name)
        self.lineEdit_ip.setText(obj.ip)
        self.lineEdit_port.setText(str(obj.port))

        
        if obj.ssl.sessreuse == 'ENABLED' :
            self.radioButton_reuse.setChecked(True)
            self.lineEdit_idletimeout.setText(str(obj.ssl.sesstimeout))
        else :
            self.radioButton_reuse.setChecked(False)
            self.lineEdit_idletimeout.setText('')


        if obj.ssl.ssl3 == 'ENABLED' :
            self.radioButton_ssl3.setChecked(True)
        else :
            self.radioButton_ssl3.setChecked(False)

        if obj.ssl.tls1 == 'ENABLED' :
            self.radioButton_tls1.setChecked(True)
        else :
            self.radioButton_tls1.setChecked(False)

        if obj.ssl.tls11 == 'ENABLED' :
            self.radioButton_tls11.setChecked(True)
        else :
            self.radioButton_tls11.setChecked(False)

        if obj.ssl.tls12 == 'ENABLED' :
            self.radioButton_tls12.setChecked(True)
        else :
            self.radioButton_tls12.setChecked(False)

        if obj.ssl.sendclosenotify == 'YES' :
            self.radioButton_sendcn.setChecked(True)
        else :
            self.radioButton_sendcn.setChecked(False)

        if obj.ssl.snienable == 'ENABLED' :
            self.radioButton_sni.setChecked(True)
        else :
            self.radioButton_sni.setChecked(False)


        if obj.ssl.clientauth == 'DISABLED' :
            obj.ssl.clientcert = None
            curidx = 0
        else :
            if obj.ssl.clientcert == 'Mandatory' :
                curidx = 1
            else :
                curidx = 2
        self.comboBox_cauth.setCurrentIndex(curidx)


        if obj.ssl.pushenctrigger == 'Always' :
            self.comboBox_push.setCurrentIndex(0)
        elif obj.ssl.pushenctrigger == 'Ignore' :
            self.comboBox_push.setCurrentIndex(1)
        elif obj.ssl.pushenctrigger == 'Merge' :
            self.comboBox_push.setCurrentIndex(2)
        elif obj.ssl.pushenctrigger == 'Timer' :
            self.comboBox_push.setCurrentIndex(3)


        if obj.ssl.dh == 'ENABLED' :
            self.lineEdit_dhfile.setText(obj.ssl.dhfile)
            self.lineEdit_dhcount.setText(str(obj.ssl.dhcount))
            self.radioButton_dh.setChecked(True)
        else :
            obj.ssl.dhfile = None
            self.lineEdit_dhfile.setText('')
            self.lineEdit_dhcount.setText('')
            self.radioButton_dh.setChecked(False)

        if obj.ssl.ersa == 'ENABLED' :
            self.lineEdit_ersacount.setText(str(obj.ssl.ersacount))
            self.radioButton_ersa.setChecked(True)
        else :
            self.lineEdit_ersacount.setText('')
            self.radioButton_ersa.setChecked(False)

        clist = obj.calist
        for c in clist :
            self.listWidget_ca_cert.AddToList(c)
            self.CACertAdded(c)

        clist = obj.snilist
        for c in clist :
            self.listWidget_sni_cert.AddToList(c)
            self.SNICertAdded(c)

        clist = obj.servercert
        if clist :
            self.listWidget_server_cert.AddToList(clist)
            self.ServerCertAdded(clist)

        self.FillBoundCiphers()

      

    def UpdateEntity(self,obj) :
        ret = True
        srvrcertlist = []
        snicertlist  = []
        cacertlist   = []
        dut = self.GetCurDUT()

        vname = self.lineEdit_name.text()
        test_util.GetVsrvrCertkeyBindings(dut.sess,vname,srvrcertlist,snicertlist,cacertlist)

        lw = self.listWidget_ca_cert
        li = lw.findItems('*', QtCore.Qt.MatchWildcard)
        l2 = [l.text() for l in li]
        s1 = set(cacertlist)
        s2 = set(l2)
        al = list(s2 - s1)
        dl = list(s1 - s2)
        obj.calist = l2
        
        lw = self.listWidget_sni_cert
        li = lw.findItems('*', QtCore.Qt.MatchWildcard)
        l2 = [l.text() for l in li]
        s1 = set(snicertlist)
        s2 = set(l2)
        al = list(s2 - s1)
        dl = list(s1 - s2)
        obj.snilist = l2
        
        lw = self.listWidget_server_cert
        li = lw.findItems('*', QtCore.Qt.MatchWildcard)
        l2 = [l.text() for l in li]
        if len(l2) > 0 :
            obj.servercert = l2[0]

        if self.radioButton_reuse.isChecked() :
            obj.ssl.sessreuse = 'ENABLED'
            try :
                obj.ssl.sesstimeout = int(self.lineEdit_idletimeout.text())
            except ValueError as e :
                obj.ssl.sesstimeout = 120
                self.lineEdit_idletimeout.setText('120')
        else :
            obj.ssl.sessreuse = 'DISABLED'
            obj.ssl.sesstimeout = None
            self.lineEdit_idletimeout.setText('')


        if self.radioButton_ssl3.isChecked() :
            obj.ssl.ssl3 = 'ENABLED'
        else :
            obj.ssl.ssl3 = 'DISABLED'


        if self.radioButton_tls1.isChecked() :
            obj.ssl.tls1 = 'ENABLED'
        else :
            obj.ssl.tls1 = 'DISABLED'

        if self.radioButton_tls11.isChecked() :
            obj.ssl.tls11 = 'ENABLED'
        else :
            obj.ssl.tls11 = 'DISABLED'

        if self.radioButton_tls12.isChecked() :
            obj.ssl.tls12 = 'ENABLED'
        else :
            obj.ssl.tls12 = 'DISABLED'


        if self.radioButton_sendcn.isChecked() :
            obj.ssl.sendclosenotify = 'YES'
        else :
            obj.ssl.sendclosenotify = 'NO'


        if self.radioButton_sni.isChecked() :
            obj.ssl.snienable = 'ENABLED'
        else :
            obj.ssl.snienable = 'DISABLED'



        v = self.comboBox_cauth.currentIndex()
        if v > 0 :
            obj.ssl.clientauth = 'ENABLED'
            if v == 1 :
                obj.ssl.clientcert = 'Mandatory'
            elif v == 2 :
                obj.ssl.clientcert = 'Optional'
        else :
            obj.ssl.clientauth = 'DISABLED'
            obj.ssl.clientcert = None


        obj.ssl.pushenctrigger = self.comboBox_push.currentText()

        if self.radioButton_dh.isChecked() :
            obj.ssl.dh = 'ENABLED'
            obj.ssl.dhfile = self.lineEdit_dhfile.text()
            try :
                dhcount = int(self.lineEdit_dhcount.text())
            except ValueError as e :
                dhcount = 0
            
            obj.ssl.dhcount = dhcount
            self.lineEdit_dhcount.setText(str(dhcount))
        else :
            obj.ssl.dh = 'DISABLED'
            obj.ssl.dhfile = None
            obj.ssl.dhcount = None


        if self.radioButton_ersa.isChecked() :
            obj.ssl.ersa = 'ENABLED'
            try :
                ersacount = int(self.lineEdit_ersacount.text())
            except ValueError as e :
                ersacount = 0
            
            obj.ssl.ersacount = ersacount
            self.lineEdit_ersacount.setText(str(ersacount))
        else :
            obj.ssl.ersa = 'DISABLED'
            obj.ssl.ersacount = None


        obj.ssl.cipherurl = None
        obj.ssl.sslv2url = None
        obj.ssl.dtlsprofilename = None
        obj.ssl.sslprofile = None

        sess = self.curDUT.sess
        try :
            SSLVSERVER.sslvserver.update(sess,obj.ssl)
        except NITROEXCEPTION as e :
            print 'Update Vserver failed : {}'.format(e.message)
            ret = False
        except Exception as e :
            print 'Update Vserver failed : {}'.format(e.message)
            ret = False

        return ret




class SSLVServerEntity(QtCore.QObject):
    sigStatus = QtCore.pyqtSignal(int)
    
    def __init__(self,name,ip,port,vtype,sess,nsip=None) :
        super(self.__class__,self).__init__()
        self.name  = name
        self.ip    = ip
        self.port  = port
        self.type  = vtype
        self.lb    = None
        self.ssl   = None
        self.sess  = sess
        self.nsip = nsip
        self.calist = []
        self.snilist = []
        self.servercert = None
        self.boundciphers = []
        self.entity_type = GenericContainer.GenericContainer.TYPE_SSL_VSERVER
        self.fromfiledict = None
        self.isrunning = False
        self.boundServices = []


    def GetName(self) :
        name = self.name + '\n' + self.ip + '\n' + str(self.port)
        return name



    def Create(self) :
        sslv = LBVSERVER.lbvserver()
        sslv.name = self.name
        sslv.servicetype = self.type
        sslv.port = self.port
        sslv.ipv46 = self.ip

        try :
            self.lb  = LBVSERVER.lbvserver.add(self.sess,sslv)
            if self.lb :
                self.ssl = SSLVSERVER.sslvserver.get(self.sess,sslv.name)
            if not self.ssl :
                self.lb = None
        except NITROEXCEPTION as e :
            self.lb = None
            self.ssl = None
            print '{}'.format(e.message)
        except Exception as e :
            self.lb = None
            self.ssl = None
            print '{}'.format(e.message)

        self.boundciphers.append('DEFAULT')
        return self.ssl


    def Refresh(self) :
        try :
            if self.lb :
                self.lb  = LBVSERVER.lbvserver.get(self.sess,self.name)
        except NITROEXCEPTION as e :
            print 'SSLVserverEntity:Refresh: NitroException{}'.format(e.message)
            self.lb = None
            self.ssl = None
            print '{}'.format(e.message)
        except Exception as e :
            print 'SSLServiceEntity:Refresh: Exception{}'.format(e.message)
            self.lb = None
            self.ssl = None

        if self.lb :
            if self.lb.curstate == 'UP' :
                self.isrunning = True
            else :
                self.isrunning = False


    def Update(self) :
        d = self.fromfiledict
        
        if d['sessreuse'] == 'ENABLED' :
            self.ssl.sessreuse = 'ENABLED'
            try :
                self.ssl.sesstimeout = int(self.lineEdit_idletimeout.text())
            except ValueError as e :
                self.ssl.sesstimeout = 120
        else :
            self.ssl.sessreuse = 'DISABLED'
            self.ssl.sesstimeout = None


        if d['ssl3'] == 'ENABLED' :
            self.ssl.ssl3 = 'ENABLED'
        else :
            self.ssl.ssl3 = 'DISABLED'


        if d['tls1'] == 'ENABLED' :
            self.ssl.tls1 = 'ENABLED'
        else :
            self.ssl.tls1 = 'DISABLED'


        if d['tls11'] == 'ENABLED' :
            self.ssl.tls11 = 'ENABLED'
        else :
            self.ssl.tls11 = 'DISABLED'


        if d['tls12'] == 'ENABLED' :
            self.ssl.tls12 = 'ENABLED'
        else :
            self.ssl.tls12 = 'DISABLED'


        if d['sendclosenotify'] == 'YES' :
            self.ssl.sendclosenotify = 'YES'
        else :
            self.ssl.sendclosenotify = 'NO'


        if d['snienable'] == 'ENABLED' :
            self.ssl.snienable = 'ENABLED'
        else :
            self.ssl.snienable = 'DISABLED'


        if d['clientauth'] == 'DISABLED' :
            self.ssl.clientauth = 'DISABLED'
            self.ssl.clientcert = None
        else :
            if d['clientcert'] == 'Mandatory' :
                self.ssl.clientcert = 'Mandatory'
            else :
                self.ssl.clientcert = 'Optional'


        self.ssl.pushenctrigger = d['pushenctrigger']
        self.ssl.dh = d['dh']
        self.ssl.ersa = d['ersa']
        

        try :
            SSLVSERVER.sslvserver.update(sess,self.ssl)
        except NITROEXCEPTION as e :
            print 'Update Vserver failed : {}'.format(e.message)
            ret = False
        except Exception as e :
            print 'Update Vserver failed : {}'.format(e.message)
            ret = False



    def Delete(self) :
        sslv = LBVSERVER.lbvserver()
        sslv.name = self.name
        sslv.servicetype = self.type
        sslv.port = self.port
        sslv.ipv46 = self.ip

        #self.sess.relogin()
        try :
            LBVSERVER.lbvserver.delete(self.sess,sslv)
        except NITROEXCEPTION as e :
            self.lb = None
            self.ssl = None
            print '{}'.format(e.message)
        except Exception as e :
            self.lb = None
            self.ssl = None
            print '{}'.format(e.message)



    def UpDownSlot(self, i) :
        if i > 0 :
            self.isRunning = True
        else :
            self.isRunning = False
      

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



    def Get(self) :
        self.lb = LBVSERVER.lbvserver.add(self.sess,self.name)
        self.ssl = SSLVSERVER.sslvserver.get(sess,self.name)
        return self.ssl

    def GetType(self) :
        return self.entity_type


    def ToJson(self) :
        d = dict()
        d['name'] = self.name
        d['ip'] = self.ip
        d['nsip'] = self.nsip
        d['port']  = self.port
        d['type']  = self.type
        d['calist'] = self.calist
        d['snilist'] = self.snilist
        d['servercert'] = self.servercert
        d['sessreuse'] = self.ssl.sessreuse
        d['sesstimeout'] = self.ssl.sesstimeout
        d['ssl3']   = self.ssl.ssl3
        d['tls1']   = self.ssl.tls1
        d['tls11'] = self.ssl.tls11
        d['tls12'] = self.ssl.tls12
        d['sendclosenotify']       = self.ssl.sendclosenotify
        d['clientauth']  = self.ssl.clientauth
        d['clientcert'] =  self.ssl.clientcert
        d['pushenctrigger'] = self.ssl.pushenctrigger
        d['dh'] = self.ssl.dh
        d['dhfile'] = self.ssl.dhfile
        d['dhcount']  =  self.ssl.dhcount
        d['ersa']  =  self.ssl.ersa
        d['ersacount']  =  self.ssl.ersacount
        d['boundciphers'] = self.boundciphers
        d['snienable'] = self.ssl.snienable

        s = json.dumps(d)
        return s



    def ToFileStr(self) :
        js = self.ToJson()
        d = dict()
        d['type'] = self.entity_type
        d['val'] = js
        s = json.dumps(d)
        return s



    def PrepareMimeData(self,ccode=None) :
        d = dict()
        d['type'] = self.entity_type
        d['name'] = self.name
        d['ip'] = self.ip
        d['port'] = self.port
        d['ccode'] = ccode
        s = json.dumps(d)
        return s


    def AllowDrop(self,jstring) :
        d = json.loads(jstring)
        t = d['type']
        if ((t == GenericContainer.GenericContainer.TYPE_SSL_SERVICE) or (t == GenericContainer.GenericContainer.TYPE_HTTP_SERVICE)):
            return True
        else :
            return False
        

    def HandleDropEvent(self,jstring) :
        d = json.loads(jstring)
        svcname = d['name']
        bndg = LBVSRVRSVC.lbvserver_service_binding()
        bndg.name = self.name
        bndg.servicename = svcname

        try :
            LBVSRVRSVC.lbvserver_service_binding.add(self.sess,bndg)
        except NITROEXCEPTION as e :
            print 'service drop failed'
        except Exception as e :
            print 'service drop failed'
        
        return


    def GetDUTByIP(self,nsip) :
        return self.parent.GetDUTByIP(nsip)



    def ApplySavedCiphers(self,sess=None) :
        ll = SSLVSRVRCIPHERSUITE.sslvserver_sslciphersuite_binding.get(sess,self.name)
        ll = [l.ciphername for l in ll]
        set_ll = set(ll)
        set_bound = set(self.boundciphers)

        l = set_ll - set_bound
        svlist = []
        
        for x in l :
            sv = SSLVSRVRCIPHER.sslvserver_sslcipher_binding()
            sv.vservername = self.name
            sv.ciphername = str(x)
            svlist.append(sv)
            SSLVSRVRCIPHER.sslvserver_sslcipher_binding.delete(sess,sv)

        l = set_bound - set_ll
        svlist = []
        print 'Adding cipher [{}]'.format(l)
        for x in l :
            sv = SSLVSRVRCIPHER.sslvserver_sslcipher_binding()
            sv.vservername = self.name
            sv.ciphername = str(x)
            svlist.append(sv)
            SSLVSRVRCIPHER.sslvserver_sslcipher_binding.add(sess,sv)




    @classmethod
    def FromFileStr(cls,jstring,sess=None) :
        d = json.loads(jstring)
        d = json.loads(d['val'])
        nsip = d['nsip']

        try :
            
            lb = LBVSERVER.lbvserver.get(sess,d['name'])
            if(lb) :
                LBVSERVER.lbvserver.delete(sess,lb)
        except NITROEXCEPTION as e :
            pass
        except Exception as e :
            pass
        
        obj = SSLVServerEntity(d['name'],d['ip'],d['port'],d['type'],sess,nsip)
        obj.fromfiledict = d
    
        if not obj.Create() :
            print 'obj.Create() failed'
            return None

        l = d['calist']
        if len(l) > 0 :
            test_util.BindUnbindCACert(sess,d['name'],l,isunbind=False)
            obj.calist = l

        l = d['snilist']
        if len(l) > 0 :
            test_util.BindUnbindSniCert(sess,d['name'],l,isunbind=False)
            obj.snilist = l

        l = d['servercert']
        if l :
            test_util.BindUnbindServerCert(sess,d['name'],l,isunbind=False)
            obj.servercert = l[0]
        


        obj.ssl.sessreuse = d['sessreuse']
        obj.ssl.sesstimeout = d['sesstimeout'] 
        obj.ssl.ssl3  = d['ssl3']
        obj.ssl.tls1   = d['tls1']
        obj.ssl.tls11 = d['tls11']
        obj.ssl.tls12 = d['tls12']
        obj.ssl.sendclosenotify = d['sendclosenotify']
        obj.ssl.clientauth = d['clientauth']
        obj.ssl.clientcert = d['clientcert'] 
        obj.ssl.pushenctrigger = d['pushenctrigger']
        obj.ssl.dh = d['dh']
        obj.ssl.dhfile = d['dhfile']
        obj.ssl.dhcount = d['dhcount'] 
        obj.ssl.ersa = d['ersa']
        obj.ssl.ersacount = d['ersacount']
        obj.ssl.snienable = d['snienable']
        obj.boundciphers = d['boundciphers']

        obj.ssl.cipherurl = None
        obj.ssl.sslv2url = None
        obj.ssl.dtlsprofilename = None
        obj.ssl.sslprofile = None


        obj.ApplySavedCiphers(sess)

        try :
            SSLVSERVER.sslvserver.update(sess,obj.ssl)
        except NITROEXCEPTION as e :
            print 'Update Vserver failed : {}'.format(e.message)
            ret = False
        except Exception as e :
            print 'Update Vserver failed : {}'.format(e.message)
            ret = False


        return obj






if __name__ == "__main__":
    sess = test_util.Login('10.102.28.201')
    l = SSLVSRVRCIPHER.sslvserver_sslcipher_binding.get(sess,'vone')
    l = SSLVSRVRCIPHERSUITE.sslvserver_sslciphersuite_binding.get(sess,'vone')
    for x in l :
        print '{}  {} '.format(x.vservername,x.ciphername)
    
