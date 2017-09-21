# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MasterContainer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')
from PyQt5 import QtCore, QtGui, QtWidgets
from GenericContainer import *
from DUTDialog import *
from CounterList import *


class MasterContainer(QtWidgets.QWidget):
    
    def setupUi(self):
        Form.setObjectName("Form")
        Form.resize(607, 573)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(1,1,1,1)
        self.horizontalLayout.setSpacing(2)
        
        self.L1 = GenericContainer(GenericContainer.CONTAINER_L1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L1.sizePolicy().hasHeightForWidth())
        self.L1.setSizePolicy(sizePolicy)
        #self.L1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.L1.setObjectName("L1")
        self.horizontalLayout.addWidget(self.L1)
        self.L1.show()
        
        
        self.L2 = GenericContainer(GenericContainer.CONTAINER_L2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L2.sizePolicy().hasHeightForWidth())
        self.L2.setSizePolicy(sizePolicy)
        self.L2.setAccessibleDescription("")
        self.L2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.L2.setObjectName("L2")
        self.horizontalLayout.addWidget(self.L2)

        
        self.T1_NS = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.T1_NS.sizePolicy().hasHeightForWidth())
        self.T1_NS.setSizePolicy(sizePolicy)
        self.T1_NS.setObjectName("T1_NS")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.T1_NS)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(2)
        
        self.T1 = GenericContainer(GenericContainer.CONTAINER_T1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.T1.sizePolicy().hasHeightForWidth())
        self.T1.setSizePolicy(sizePolicy)
        self.T1.setStyleSheet("background-color: rgb(170, 170, 170);")

        self.T1.setObjectName("T1")
        self.verticalLayout.addWidget(self.T1)

        
        self.NS = GenericContainer(GenericContainer.CONTAINER_NS)
        self.NS = self.GetCounterWidget()
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(8)
        sizePolicy.setHeightForWidth(self.NS.sizePolicy().hasHeightForWidth())
        self.NS.setSizePolicy(sizePolicy)
        self.NS.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.NS.setObjectName("NS")
        self.verticalLayout.addWidget(self.NS)

        
        self.L2.raise_()
        self.T1.raise_()
        self.NS.raise_()
        self.T1_NS.raise_()
        self.horizontalLayout.addWidget(self.T1_NS)

        
        self.R2 = GenericContainer(GenericContainer.CONTAINER_R2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.R2.sizePolicy().hasHeightForWidth())
        self.R2.setSizePolicy(sizePolicy)
        self.R2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.R2.setObjectName("R2")
        self.T1_NS.raise_()
        self.horizontalLayout.addWidget(self.R2)

        
        self.R1 = GenericContainer(GenericContainer.CONTAINER_R1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.R1.sizePolicy().hasHeightForWidth())
        self.R1.setSizePolicy(sizePolicy)
        self.R1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.R1.setObjectName("R1")
        self.horizontalLayout.addWidget(self.R1)
        

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.L1.setAccessibleDescription(_translate("Form", "L1"))
        self.L2.setAccessibleName(_translate("Form", "L2"))
        self.T1.setAccessibleName(_translate("Form", "T1"))
        #self.NS.setAccessibleName(_translate("Form", "NS"))
        self.R2.setAccessibleName(_translate("Form", "R2"))
        self.R1.setAccessibleName(_translate("Form", "R1"))



    def GetSess(self) :
        return self.NS.GetSess()
    


    def ReplaceNSWithCounterList(self) :
        NSCounterList.Init()

        F = FetcherThread('10.102.28.201', freq=0)
        F.AddCounters(NSCounterList.COUNTERS)
        F.Chunkify(5)

        w = NSCounterHarnessWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(8)
        sizePolicy.setHeightForWidth(self.NS.sizePolicy().hasHeightForWidth())
        w.setSizePolicy(sizePolicy)

        w.SetFetcherThread(F)
        w.AddCounter('ssl_cur_sslInfo_SPCBInUseCount')
        w.AddCounter('pcb_cur_inuse')
        w.SetXYScale(5.0,0.1)
        w.SetFromToTicks(0,100)

        #self.tstLayout = QtWidgets.QHBoxLayout(self.NS)
        self.verticalLayout.replaceWidget(self.NS, w)



    def GetCounterWidget(self) :
        NSCounterList.Init()
        F = FetcherThread('10.102.28.201', freq=0)
        F.AddCounters(NSCounterList.COUNTERS)
        F.Chunkify(5)
        w = NSCounterHarnessWidget()

        w.SetFetcherThread(F)
        w.AddCounter('ssl_cur_sslInfo_SPCBInUseCount')
        w.AddCounter('pcb_cur_inuse')
        w.SetXYScale(5.0,0.1)
        w.SetFromToTicks(0,100)

        return w




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = MasterContainer()
    ui = Ui_Form()
    Form.setupUi()
    #Form.ReplaceNSWithCounterList()
    Form.show()
    sys.exit(app.exec_())

