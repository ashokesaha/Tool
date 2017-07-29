# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MultiWidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import  CustomWidget

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("verticalLayout")

        self.w1 = self.PrepareWidget()
        self.w2 = self.PrepareWidget()
        self.w3 = self.PrepareWidget()

        self.horizontalLayout.addWidget(self.w1)
        self.horizontalLayout.addWidget(self.w2)
        self.horizontalLayout.addWidget(self.w3)



    def PrepareWidget(self) :
        w = QtWidgets.QWidget()
        w.setFixedWidth(50)
        w.verticalLayout = QtWidgets.QVBoxLayout(w)
        w.verticalLayout.setSizeConstraint(0)

        #w.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(60, 60, 60, 250), stop:1 rgba(250, 250, 250, 255));")
        w.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(120, 120, 120, 250), stop:1 rgba(20, 20, 20, 220));")
        #w.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(60, 60, 60, 250), stop:1 rgba(250, 250, 250, 255));")
        #w.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(60, 60, 60, 250), stop:1 rgba(250, 250, 250, 255));")
        #w.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(60, 60, 60, 250), stop:1 rgba(250, 250, 250, 255));")


        w1 = CustomWidget.MyWidget(1)
        w2 = CustomWidget.MyWidget(2)
        w3 = CustomWidget.MyWidget(3)
        w4 = CustomWidget.MyWidget(4)

        w.verticalLayout.addWidget(w1)
        w.verticalLayout.addWidget(w2)
        w.verticalLayout.addWidget(w3)
        w.verticalLayout.addWidget(w4)

        return w
        

    
    def setupUiX(self, Form):
        Form.setObjectName("Form")
        #Form.resize(40, 400)
        #Form.setFixedWidth(40)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.right_frame = Form

        self.right_frame.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(60, 60, 60, 250), stop:1 rgba(250, 250, 250, 255));")
        #self.right_frame.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(120, 120, 120, 250), stop:1 rgba(20, 20, 20, 220));")
        #self.right_frame.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(60, 60, 60, 250), stop:1 rgba(250, 250, 250, 255));")
        #self.right_frame.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(60, 60, 60, 250), stop:1 rgba(250, 250, 250, 255));")
        #self.right_frame.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(60, 60, 60, 250), stop:1 rgba(250, 250, 250, 255));")
        
        #self.right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.right_frame.setObjectName("right_frame")

        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        #sizePolicy.setHorizontalStretch(1)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.right_frame.sizePolicy().hasHeightForWidth())
        #self.right_frame.setSizePolicy(sizePolicy)
        #self.right_frame.setMinimumSize(QtCore.QSize(32, 0))

        self.verticalLayout.setSizeConstraint(0)

        w1 = CustomWidget.MyWidget(1)
        w2 = CustomWidget.MyWidget(2)
        w3 = CustomWidget.MyWidget(3)
        w4 = CustomWidget.MyWidget(4)
        w5 = CustomWidget.MyWidget(5)
        w6 = CustomWidget.MyWidget(6)
        w7 = CustomWidget.MyWidget(7)



        self.verticalLayout.addWidget(w1)
        qsz = w1.size()
        print 'w1 size {} {}'.format(qsz.width(), qsz.height())
        self.verticalLayout.addWidget(w2)
        qsz = w2.size()
        print 'w2 size {} {}'.format(qsz.width(), qsz.height())
        self.verticalLayout.addWidget(w3)
        qsz = w3.size()
        print 'w3 size {} {}'.format(qsz.width(), qsz.height())
        self.verticalLayout.addWidget(w4)
        qsz = w4.size()
        print 'w4 size {} {}'.format(qsz.width(), qsz.height())
        #self.verticalLayout.addWidget(w5)
        qsz = w5.size()
        print 'w5 size {} {}'.format(qsz.width(), qsz.height())
        #self.verticalLayout.addWidget(w6)
        qsz = w6.size()
        print 'w6 size {} {}'.format(qsz.width(), qsz.height())
        #self.verticalLayout.addWidget(w7)
        qsz = w7.size()
        print 'w7 size {} {}'.format(qsz.width(), qsz.height())
        

        #self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)





    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.right_frame.setAccessibleName(_translate("Form", "right_frame"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #Form = QtWidgets.QFrame()
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

