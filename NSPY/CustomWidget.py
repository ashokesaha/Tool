# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CustomWidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(100, 100)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))



class  MyWidget(QtWidgets.QWidget)  :
    def  __init__(self,parent=None) :
        super(self.__class__,self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")
        self.pointList = []
        self.a = 0
        self.b = 0
        self.color = QtGui.QColor(150,0,0,255)
        #gd = QRadialGradient()
        #self.brush = QBrush(gd)
        #self.brush.setColor(self.color)
        
        #self.brush.setStyle(QtCore.Qt.RadialGradientPattern)

        self.bgcolor = QtGui.QColor(0,0,0,0)
        self.bgbrush = QtGui.QBrush(self.bgcolor, QtCore.Qt.SolidPattern)

        qsz = QtCore.QSize(32,32)
        self.setMinimumSize(qsz)
        self.setMaximumSize(qsz)

    
    def mousePressEvent(self,event) :
        gx = event.globalX()
        gy = event.globalY()
        x  = event.x()
        y  = event.y()
        p1 = event.localPos()
        p2 = event.pos()
        h  = self.height()
        w  = self.width()
        p3 = self.mapToGlobal(p2)

        x -= self.a/2
        y -= self.b/2
        a  = float(self.a)/2
        b  = float(self.b)/2
        
        r1 =  float(x * x)/float(a * a)
        r2 =  float(y * y)/float(b * b)
        r  = r1 + r2
        if(r < 1.0) :
            print 'Inside'
        else :
            print 'Outside'


        alpha = self.color.alpha() - 10
        if alpha < 0 :
            alpha = 0
        
        self.color.setAlpha(alpha)
        self.brush.setColor(self.color)

        self.update()



    def  paintEvent(self, event=None) :
        r  = self.rect()
        h  = r.height()
        w  = r.width()

        qP = QtGui.QPainter(self)
        qP.setPen(QtCore.Qt.NoPen)
        qP.setRenderHint(QtGui.QPainter.Antialiasing)

        qP.setBrush(self.bgbrush)
        qP.drawRect(r)
        
        if((w - 4) > (h - 4)) :
            self.a = h - 4
        else :
            self.a = w - 4

        self.b = self.a
        #print 'PaintEvent: size {}'.format(self.a)

        #c1 = QtGui.QColor(50,0,0,250)
        #c2 = QtGui.QColor(200,0,0,250)

        #c1 = QtGui.QColor(0,50,0,250)
        #c2 = QtGui.QColor(0,0200,0,250)

        #c1 = QtGui.QColor(0,0,50,250)
        #c2 = QtGui.QColor(0,0,200,250)

        #c1 = QtGui.QColor(50,50,50,250)
        #c2 = QtGui.QColor(200,200,200,250)

        #c1 = QtGui.QColor(50,10,10,250)
        #c2 = QtGui.QColor(200,40,40,250)

        #c1 = QtGui.QColor(0,50,50,250)
        #c2 = QtGui.QColor(0,200,200,250)

        #c1 = QtGui.QColor(30,50,0,250)
        #c2 = QtGui.QColor(120,200,0,250)

        #c1 = QtGui.QColor(50,0,50,250)
        #c2 = QtGui.QColor(200,0,200,250)

        c1 = QtGui.QColor(50,80,50,250)
        c2 = QtGui.QColor(200,240,200,250)



        
        gd = QtGui.QRadialGradient(2+self.a/2, 2+self.a/2, self.a/2)
        gd.setColorAt(0,c2)
        gd.setColorAt(1,c1)
        
        
        self.brush = QtGui.QBrush(gd)
        #self.brush.setColor(self.color)
        qP.setBrush(self.brush)
        qP.drawEllipse(2,2,self.a,self.b)



    def sizeHint(self) :
        #print 'sizeHint called'
        qsz = QtCore.QSize(32,32)
        return qsz

    

    


    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

