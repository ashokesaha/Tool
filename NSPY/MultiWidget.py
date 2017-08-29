# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MultiWidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import CustomWidget

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(432, 400)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_frame = QtWidgets.QFrame(Form)
        #self.left_frame.setStyleSheet("background-color: rgb(255, 255, 0);")
        #self.left_frame.setStyleSheet("background-color: rgb(156, 156, 156);")
        self.left_frame.setStyleSheet("background-color: rgb(181, 181, 181);\n"
"background-color: qlineargradient(spread:pad, x1:0.955, y1:0, x2:1, y2:0, stop:0 rgba(158, 158, 158, 255), stop:1 rgba(255, 255, 255, 255));")
        self.left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_frame.setObjectName("left_frame")
        self.left_widget = CustomWidget.MyWidget(self.left_frame)
        self.left_widget.setGeometry(QtCore.QRect(40, 160, 80, 80))
        self.left_widget.setObjectName("left_widget")
        self.horizontalLayout.addWidget(self.left_frame)
        self.right_frame = QtWidgets.QFrame(Form)
        #self.right_frame.setStyleSheet("background-color: rgb(255, 85, 127);")
        #self.right_frame.setStyleSheet("background-color: rgb(223, 223, 223);")
        self.right_frame.setStyleSheet("background-color: rgb(181, 181, 181);\n"
"background-color: qlineargradient(spread:pad, x1:0.955, y1:0, x2:1, y2:0, stop:0 rgba(158, 158, 158, 255), stop:1 rgba(255, 255, 255, 255));")
        self.right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.right_frame.setObjectName("right_frame")
        self.right_widget = CustomWidget.MyWidget(self.right_frame)
        self.right_widget.setGeometry(QtCore.QRect(40, 160, 80, 80))
        self.right_widget.setObjectName("right_widget")
        self.horizontalLayout.addWidget(self.right_frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.left_frame.setAccessibleName(_translate("Form", "left_frame"))
        self.left_frame.setAccessibleDescription(_translate("Form", "left_frame"))
        self.left_widget.setAccessibleName(_translate("Form", "left_widget"))
        self.right_frame.setAccessibleName(_translate("Form", "right_frame"))
        self.right_widget.setAccessibleName(_translate("Form", "right_widget"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

