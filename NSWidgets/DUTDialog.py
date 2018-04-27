# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DUT.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
from   PyQt5 import QtCore, QtGui, QtWidgets
import test_util
import CertInstaller
import TestException
import CustomWidget
import MasterContainer
import AllocFree

from   nssrc.com.citrix.netscaler.nitro.service.nitro_service  import *
import nssrc.com.citrix.netscaler.nitro.resource.config.ns.nshardware as NSHW
import nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip as NS
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as CERTKEY
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher as CIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslciphersuite as CIPHERSUITE


class DUTDialog(object):
    def  __init__(self,container) :
        self.container = container
        self.ccode = container.ccode
        self.workerThread = None
        self.workerObj = None

    
    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("DUTDialog")
        Dialog.resize(598, 571)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")

        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        
        self.lineedit_nsip = QtWidgets.QLineEdit(Dialog)
        self.lineedit_nsip.setObjectName("lineedit_nsip")
        self.gridLayout.addWidget(self.lineedit_nsip, 0, 0, 1, 1)
        
        self.lineedit_qntmsize = QtWidgets.QLineEdit(Dialog)
        self.lineedit_qntmsize.setObjectName("lineedit_qntmsize")
        self.gridLayout.addWidget(self.lineedit_qntmsize, 0, 1, 1, 1)
        
        self.lineedit_qntmtime = QtWidgets.QLineEdit(Dialog)
        self.lineedit_qntmtime.setObjectName("lineedit_qntmtime")
        self.gridLayout.addWidget(self.lineedit_qntmtime, 0, 2, 1, 1)
        
        self.lineedit_pktcount = QtWidgets.QLineEdit(Dialog)
        self.lineedit_pktcount.setObjectName("lineedit_pktcount")
        self.gridLayout.addWidget(self.lineedit_pktcount, 0, 3, 1, 1)
        
        self.combobox_reneg = QtWidgets.QComboBox(Dialog)
        self.combobox_reneg.setObjectName("combobox_reneg")
        self.combobox_reneg.addItem("")
        self.combobox_reneg.addItem("")
        self.gridLayout.addWidget(self.combobox_reneg, 1, 0, 1, 1)
        
        self.combobox_push = QtWidgets.QComboBox(Dialog)
        self.combobox_push.setObjectName("combobox_push")
        self.combobox_push.addItem("")
        self.combobox_push.addItem("")
        self.combobox_push.addItem("")
        self.combobox_push.addItem("")
        self.gridLayout.addWidget(self.combobox_push, 1, 1, 1, 1)
        
        spacerItem = QtWidgets.QSpacerItem(188, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 2)

        
        self.widget_nsstats = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(9)
        sizePolicy.setHeightForWidth(self.widget_nsstats.sizePolicy().hasHeightForWidth())
        self.widget_nsstats.setSizePolicy(sizePolicy)
        self.widget_nsstats.setStyleSheet("background-color: rgb(100, 168, 168);")
        self.widget_nsstats.setObjectName("widget_nsstats")

        self.verticalLayout.addLayout(self.gridLayout)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")


        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.buttonBox)
        
        self.buttonBox.raise_()
        self.lineedit_nsip.raise_()
        self.lineedit_qntmsize.raise_()
        self.lineedit_qntmtime.raise_()
        self.combobox_reneg.raise_()
        self.lineedit_pktcount.raise_()
        self.combobox_push.raise_()
        self.widget_nsstats.raise_()
        self.widget_nsstats.raise_()

        if self.container.backend_obj :
            self.FillFromObj(self.container.backend_obj)
            Form = AllocFree.AllocFreeForm(plotwidth=2)
            W = AllocFree.AllocFreeWorker()
            self.workerObj = W
            W.SetNSIP(self.container.backend_obj.nsip)
            W.AddCounters(Form.ListCounters())
            T = QtCore.QThread()
            self.workerThread = T
            W.moveToThread(T)
            T.started.connect(W.process)
            W.finished.connect(T.terminate)
            W.results.connect(Form.UpdateResults)
            self.verticalLayout.addWidget(Form)
            #self.horizontalLayout.addWidget(Form)
            Form.setStyleSheet("background-color: rgb(168, 168, 168);")
            T.start()

            Form2 = AllocFree.RateCounters(plotwidth=2)
            W2 = AllocFree.AllocFreeWorker()
            self.workerObj2 = W2
            W2.SetNSIP(self.container.backend_obj.nsip)
            W2.AddCounters(Form2.ListCounters())
            T2 = QtCore.QThread()
            self.workerThread2 = T2
            W2.moveToThread(T2)
            T2.started.connect(W2.process)
            W2.finished.connect(T2.terminate)
            W2.results.connect(Form2.UpdateResults)
            self.verticalLayout.addWidget(Form2)
            T2.start()
            
        else :
            self.verticalLayout.addWidget(self.widget_nsstats)
            #self.horizontalLayout.addWidget(self.widget_nsstats)
            self.widget_nsstats.setStyleSheet("background-color: rgb(168, 168, 168);")


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineedit_nsip.setPlaceholderText(_translate("Dialog", "NSIP"))
        self.lineedit_qntmsize.setPlaceholderText(_translate("Dialog", "Quantum Size"))
        self.lineedit_qntmtime.setPlaceholderText(_translate("Dialog", "Quantum Timeout"))
        self.lineedit_pktcount.setPlaceholderText(_translate("Dialog", "Packet Trigger"))
        self.combobox_reneg.setItemText(0, _translate("Dialog", "Deny Reneg"))
        self.combobox_reneg.setItemText(1, _translate("Dialog", "Allow Reneg"))
        self.combobox_push.setItemText(0, _translate("Dialog", "PUSH 1"))
        self.combobox_push.setItemText(1, _translate("Dialog", "PUSH 2"))
        self.combobox_push.setItemText(2, _translate("Dialog", "PUSH 3"))
        self.combobox_push.setItemText(3, _translate("Dialog", "PUSH 4"))



    def  accept(self) :
        try :
            e = self.BuildEntity()
            if not e :
                print 'entity creation failed'
                raise TestException.TestException(1)
            e.ccode = self.ccode
            test_util.AddTCPMonitor(e.sess,'quick_mon')

        except TestException.TestException as e :
            plt = self.lineedit_nsip.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.lineedit_nsip.setPalette(plt)
            self.lineedit_nsip.cursorPositionChanged.connect(self.cursorPositionChanged)
            return
        
        self.container.SetBackendObj(e)
        self.container.AddDUT(e)

        if self.workerObj:
            self.workerObj.dostop = True
            QtCore.QThread.yieldCurrentThread()
            while self.workerThread.isRunning() :
                print 'QThread still running'
                #QtCore.QThread.sleep(1)
                self.workerThread.wait()
                
        
        self.dialog.accept()


    def  reject(self) :
        if self.workerObj:
            self.workerObj.dostop = True
            while self.workerThread.isRunning() :
                print 'QThread still running'
                #QtCore.QThread.sleep(1)
                self.workerThread.wait()

        self.dialog.reject()
    



    def cursorPositionChanged(self,old,new) :
        plt = self.lineedit_nsip.palette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        self.lineedit_nsip.setPalette(plt)
        self.lineedit_nsip.cursorPositionChanged.disconnect()



    def BuildEntity(self) :
        try :
            qntmsize = int(self.lineedit_qntmsize.text())
        except ValueError as e :
            qntmsize = 0

        try :
            qntmtime = int(self.lineedit_qntmtime.text())
        except ValueError as e :
            qntmtime = 0

        try :
            pktcount = int(self.lineedit_pktcount.text())
        except ValueError as e :
            pktcount = 0


        entity = DUTEntity(self.lineedit_nsip.text(),
                           qntmsize,qntmtime,pktcount,
                           self.combobox_reneg.currentIndex(),
                           self.combobox_push.currentIndex(),self.ccode )

        sess = entity.Login()
        if not sess :
            return None
        entity.FillCerts()
        entity.FillCiphers()
        entity.FillCipherSuites()
                 
        return entity



    def FillFromObj(self,obj) :
        self.lineedit_nsip.setText(obj.nsip)
        if obj.qntmsz != 0 :
            self.lineedit_qntmsize.setText(str(obj.qntmsz))
        if obj.qntmtime != 0 :
            self.lineedit_qntmtime.setText(str(obj.qntmtime))
        if obj.pktcount != 0 :
            self.lineedit_pktcount.setText(str(obj.pktcount))
        self.combobox_reneg.setCurrentIndex(obj.denyreneg)
        self.combobox_push.setCurrentIndex(obj.pushopt)
        self.lineedit_nsip.setReadOnly(True)


    def GetDialog(self) :
        return self.dialog






class DUTEntity(object):
    def __init__(self,nsip,qntmsz,qntmtime,pktcount,denyreneg,pushopt,ccode) :
        self.nsip = nsip
        self.qntmsz = qntmsz
        self.qntmtime = qntmtime
        self.pktcount = pktcount
        self.denyreneg = denyreneg
        self.pushopt = pushopt
        self.sess = None
        self.ci = None
        self.hwdescription = None
        self.vip = None
        self.snip = None
        self.logReader = None
        self.ccode = ccode

        self.allciphers = None
        self.allciphersuites = None
        self.allcerts = None
        

    def IsRunning(self) :
        return False


    def Login(self) :
        self.sess = test_util.Login(self.nsip)
        if self.sess :
            d = test_util.GetNSIPS(self.sess)
            self.vip  = d[NS.nsip.Type.VIP]
            self.snip = d[NS.nsip.Type.SNIP]
            
            hw = NSHW.nshardware.get(self.sess)
            self.hwdescription = hw[0].hwdescription
        return self.sess


    def Logout(self) :
        self.sess.logout()
        self.sess = None
        

    def InstallCerts(self) :
        self.ci = CertInstaller.CertInstall()
        self.ci.SetCertDir('C:\\Users\\ashokes\\Miniconda2\\NSPY\\Certs')
        l1 = self.ci.ListEntityCerts()
        l2 = self.ci.ListCACerts()
        self.ci.PushToNS(self.nsip)

        self.ci.AddDelEntityCerts(self.sess,0)
        self.ci.AddDelCACerts(self.sess,0)

        self.ci.LinkUnlinkCACerts(self.sess,0)
        self.ci.LinkUnlinkEntityCerts(self.sess,0)

        self.FillCerts()

        #self.Login()
        test_util.AddTCPMonitor(self.sess,'quick_mon')

    
    def ClearConfig(self) :
        sess = nitro_service(self.nsip)
        sess.set_credential('nsroot','nsroot')
        sess.clear_config(level='basic')
        self.FillCerts()
        sess.logout()
    

    def GetSess(self) :
        return self.sess


    def FillCerts(self) :
        self.allcerts = CertInstaller.CertInstall.ListCertsFromNS(self.sess)
        print 'FillCerts called for {}'.format(self.nsip)
        print 'certlists {}'.format(self.allcerts)


    def FillCiphers(self) :
        self.allciphers = CIPHER.sslcipher.get(self.sess)
        

    def FillCipherSuites(self) :
        self.allciphersuites = CIPHERSUITE.sslciphersuite.get(self.sess)

    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = DUTDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

