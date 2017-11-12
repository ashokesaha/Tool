# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ResultDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class ResultDialog(object):
    def  __init__(self,container) :
        self.container = container
        self.curDUT = container.GetCurDUT()

    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(660, 424)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")

##        self.tableWidget = QtWidgets.QTableWidget(Dialog)
##        self.tableWidget.setObjectName("tableWidget")
##        self.tableWidget.setColumnCount(0)
##        self.tableWidget.setRowCount(0)
##        self.horizontalLayout.addWidget(self.tableWidget)

        obj = self.container.GetBackendObj()
        tw = obj.PrepareResult()
        self.tableWidget = tw
        self.horizontalLayout.addWidget(self.tableWidget)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

