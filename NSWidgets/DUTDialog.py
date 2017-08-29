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
from   nssrc.com.citrix.netscaler.nitro.service.nitro_service  import *
import TestException


class DUTDialog(object):
    def  __init__(self,container) :
        self.container = container

    
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
        self.widget_nsstats.setStyleSheet("background-color: rgb(168, 168, 168);")
        self.widget_nsstats.setObjectName("widget_nsstats")

        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.widget_nsstats)

        
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

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.dialog.reject)



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
                raise TestException(1)
            if not e.Login() :
                print 'entity connect failed'
                raise TestException(1)
        except TestException.TestException as e :
            plt = self.lineedit_nsip.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.lineedit_nsip.setPalette(plt)
            self.lineedit_nsip.cursorPositionChanged.connect(self.cursorPositionChanged)
            return
        self.container.SetBackendObj(e)
        self.dialog.accept()



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
                           self.combobox_push.currentIndex() )
                           
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
    def __init__(self,nsip,qntmsz,qntmtime,pktcount,denyreneg,pushopt) :
        self.nsip = nsip
        self.qntmsz = qntmsz
        self.qntmtime = qntmtime
        self.pktcount = pktcount
        self.denyreneg = denyreneg
        self.pushopt = pushopt
        self.sess = None
        self.ci = None


    def Login(self) :
        self.sess = test_util.Login(self.nsip)
        print 'DUTEntity login to {}'.format(self.nsip)
        return self.sess


    def Logout(self) :
        print 'DUTDialog login {}'.format(self.sess.isLogin())
        self.sess.logout()
        print 'DUTDialog login {}'.format(self.sess.isLogin())
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

    
    def ClearConfig(self) :
        sess = nitro_service(self.nsip)
        sess.set_credential('nsroot','nsroot')
        sess.clear_config(level='basic')
        sess.logout()
    

    def GetSess(self) :
        return self.sess


    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = DUTDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

