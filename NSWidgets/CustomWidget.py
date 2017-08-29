# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CustomWidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from BEOpenSSLServerDialog import *
import BasicClientDialog


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(100, 100)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))



class  MyRadialWidget(QtWidgets.QWidget)  :

    SSL_VSERVER         = 1
    SSL_TCP_vserver     = 2
    HTTP_VSERVER        = 3
    SSL_SERVICE         = 4
    SSL_TCP_SERVICE     = 5
    HTTP_SERVICE        = 6
        
    
    def  __init__(self, type, parent=None):
        super(self.__class__,self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")
        self.colorList = []
        self.a = None
        self.setColors()
        if ((type < MyRadialWidget.SSL_VSERVER) or (type > MyRadialWidget.HTTP_SERVICE)) :
            type = MyRadialWidget.SSL_VSERVER
            
        self.entity_color = self.getEntityColor(type)
        self.bgcolor = QtGui.QColor(0,0,0,0)
        self.bgbrush = QtGui.QBrush(self.bgcolor, QtCore.Qt.SolidPattern)

        qsz = QtCore.QSize(32,32)
        self.setMinimumSize(qsz)
        self.setMaximumSize(qsz)


    def mousePressEvent(self,event) :
        x  = event.x()
        y  = event.y()

        x -= self.a/2
        y -= self.b/2
        a  = float(self.a)/2
        b  = float(self.b)/2
        
        r1 =  float(x * x)/float(a * a)
        r2 =  float(y * y)/float(b * b)
        r  = r1 + r2
        if(r < 1.0) :
            print 'Inside'
            self.handleMousePress(event)
        else :
            print 'Outside'


    def  handleMousePress(self,event) :
        pass

    def  getEntityColor(self,type) :
        for ec in self.colorList :
            if ec.type == type :
                return ec
        return None


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

        gd = QtGui.QRadialGradient(2+self.a/2, 2+self.a/2, self.a/2)
        gd.setColorAt(0,self.entity_color.c2)
        gd.setColorAt(1,self.entity_color.c1)
        self.brush = QtGui.QBrush(gd)
        qP.setBrush(self.brush)
        qP.drawEllipse(2,2,self.a,self.a)


    def  setColors(self) :
        c1 = QtGui.QColor(50,0,0,250)
        c2 = QtGui.QColor(200,0,0,250)
        c  = EntityColor(1,c1,c2)
        self.colorList.append(c)

        c1 = QtGui.QColor(0,50,0,250)
        c2 = QtGui.QColor(0,0200,0,250)
        c  = EntityColor(2,c1,c2)
        self.colorList.append(c)

        c1 = QtGui.QColor(0,0,50,250)
        c2 = QtGui.QColor(0,0,200,250)
        c  = EntityColor(3,c1,c2)
        self.colorList.append(c)

        c1 = QtGui.QColor(50,50,50,250)
        c2 = QtGui.QColor(200,200,200,250)
        c  = EntityColor(4,c1,c2)
        self.colorList.append(c)

        c1 = QtGui.QColor(50,10,10,250)
        c2 = QtGui.QColor(200,40,40,250)
        c  = EntityColor(5,c1,c2)
        self.colorList.append(c)

        c1 = QtGui.QColor(0,50,50,250)
        c2 = QtGui.QColor(0,200,200,250)
        c  = EntityColor(6,c1,c2)
        self.colorList.append(c)

        c1 = QtGui.QColor(30,50,0,250)
        c2 = QtGui.QColor(120,200,0,250)
        c  = EntityColor(7,c1,c2)
        self.colorList.append(c)

        c1 = QtGui.QColor(50,0,50,250)
        c2 = QtGui.QColor(200,0,200,250)
        c  = EntityColor(8,c1,c2)
        self.colorList.append(c)

        c1 = QtGui.QColor(50,90,50,250)
        c2 = QtGui.QColor(200,240,200,250)
        c  = EntityColor(9,c1,c2)
        self.colorList.append(c)

        
    def sizeHint(self) :
        #print 'sizeHint called'
        qsz = QtCore.QSize(32,32)
        return qsz


class  EntityColor() :
    def  __init__(self, type, c1, c2) :
        self.type = type
        self.c1 = c1
        self.c2 = c2





    



class  MyRectWidget(QtWidgets.QWidget) :

    INSTANCE_COUNT = 0
    
    def  __init__(self, type, parent=None):
        super(self.__class__,self).__init__(parent)
        MyRectWidget.INSTANCE_COUNT += 1
        self.instanceId = MyRectWidget.INSTANCE_COUNT
        self.type = type
        self.container = None
        qsz = QtCore.QSize(64,32)
        self.setMinimumSize(qsz)
        self.setMaximumSize(qsz)
        
        self.styleSheets = []
        self.styleSheets.append("")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(93, 80, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(0, 100,100, 255), stop:1 rgba(100, 255, 255, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(100, 0,100, 255), stop:1 rgba(255, 100, 255, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(400, 100,400, 255), stop:1 rgba(100, 100, 255, 100));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(255, 255, 0, 255), stop:1 rgba(255, 255, 200, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(0, 0, 255, 255), stop:1 rgba(100, 100, 255, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(255, 85, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(0, 200, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(0, 200, 0, 255), stop:1 rgba(200, 255, 200, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(0, 0, 255, 255), stop:1 rgba(100, 100, 255, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(255, 85, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(0, 200, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.styleSheets.append("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0.367232 rgba(0, 200, 0, 255), stop:1 rgba(200, 255, 200, 255));")

        self.backend_obj = None
        self.up = 0
        self.Th = None


    def GetType(self) :
        return self.type


    def sizeHint(self) :
        qsz = QtCore.QSize(64,32)
        return qsz

##    def mousePressEvent(self,event) :
##        print 'mousePressEvent..'
##        if self.up :
##            self.up = 0
##        else :
##            self.up = 1
##        self.repaint(self.rect())


    def contextMenuEvent(self, event) :
        menu = QtWidgets.QMenu(self)
        stopAct = startAct = None
        delAct = menu.addAction('Delete')
        propAct = menu.addAction('Properties')

        obj = self.GetBackendObj()
        if obj :
            if obj.isrunning :
                stopAct = menu.addAction('Stop')
            else :
                startAct = menu.addAction('Start')
        

        act = menu.exec_(event.globalPos())

        if act == startAct :
            print 'selected startAct'
            self.Th = CustomWidgetThread(self)
            obj.Start()
            self.Th.start()
            
        elif act == stopAct :
            print 'selected stopAct'
            obj.Stop()
            self.Th.StopRunning()
            self.Th = None
            
        elif (act == delAct) :
            print 'selected delAct'
            pass
        
        elif (act == propAct) :
            print 'selected propAct'
            dialog = QtWidgets.QDialog()
            if (self.type == GenericContainer.GenericContainer.TYPE_BE_OPENSSL_SERVER) :
                w = BEOpenSSLServerDialog(self)
            elif (self.type == GenericContainer.GenericContainer.TYPE_FE_OPENSSL_CLIENT) :
                w = BasicClientDialog.BasicClientDialog(self)
        
            w.setupUi(dialog)
            dialog.exec_()


    def GetInstanceId(self) :
        return self.instanceId



    def paintEvent(self, event=None) :
        if self.up :
            self.UpPaintEvent(event)
        else :
            self.DownPaintEvent(event)
    

    def SetUp(self) :
        self.up = 1
        self.repaint(self.rect())

    def SetDown(self) :
        self.up = 0
        self.repaint(self.rect())
        
    
    def DownPaintEvent(self, event=None) :
        gd = QtGui.QLinearGradient(0,0,self.width(),self.height())
        gd.setStart(0,0)
        gd.setFinalStop(self.width()*3/4, self.height()*3/4)
        gd.setSpread(1)
        c1 = QtGui.QColor(0,0,200,250)
        c2 = QtGui.QColor(40,40,200,250)
        gd.setColorAt(0,c1)
        gd.setColorAt(1,c2)

        qP = QtGui.QPainter(self)
        qP.setPen(QtCore.Qt.NoPen)
        qP.setRenderHint(QtGui.QPainter.Antialiasing)

        brush = QtGui.QBrush(gd)
        qP.setBrush(brush)
        qP.drawRect(self.rect())




    def UpPaintEvent(self, event=None) :
        qP = QtGui.QPainter(self)
        brush = QtGui.QBrush(QtGui.QColor(0,0,0,250))
        qP.setBrush(brush)
        qP.drawRect(self.rect())
        
        gd = QtGui.QLinearGradient(0,0,self.width(),self.height())
        gd.setStart(0,0)
        gd.setFinalStop(self.width()*3/4, self.height()*3/4)
        gd.setSpread(1)
        c1 = QtGui.QColor(0,0,200,250)
        c2 = QtGui.QColor(40,40,200,250)
        gd.setColorAt(0,c1)
        gd.setColorAt(1,c2)

        #qP = QtGui.QPainter(self)
        qP.setPen(QtCore.Qt.NoPen)
        qP.setRenderHint(QtGui.QPainter.Antialiasing)

        brush = QtGui.QBrush(gd)
        qP.setBrush(brush)
        r = self.rect()
        #r.adjust(-5,-5,-5,-5)
        qP.drawRect(2,2,r.width()-6,r.height()-6)


    def mousePressEvent(self,event) :
        self.CheckMyThread()
    


    def SetBackendObj(self,obj) :
        self.backend_obj = obj
    

    def GetBackendObj(self) :
        return self.backend_obj


    def CheckMyThread(sel) :
        th = QtCore.QThread.currentThreadId()
        print 'CheckMyThread : ThreadId {}'.format(th)
    
    
    def __del__(self) :
        print 'entity widget destroyed {}'.format(self)





class  CustomWidgetThread(QtCore.QThread) :
    def __init__(self,wdgt) :
        super(self.__class__,self).__init__()
        #self.sig = QtCore.pyqtSignal(str)
        self.wdgt = wdgt
        self.stopRunning = False
        print str(101)

    def StopRunning(self) :
        self.stopRunning = True


    def run(self) :
        obj = self.wdgt.GetBackendObj()
        if not obj :
            return

        thid = self.wdgt.GetInstanceId()
        fname = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\' + obj.name + '_' + str(thid) + '.log'

        t0 = obj.GetSockTimeout()
        obj.SetSockTimeout(0.2)
        
        with open(fname,'a') as fp  :
            while not self.stopRunning :
                s = obj.ReadOnce()
                #print 'obj {}  s {}{}'.format(obj,type(s),s)
                if s :
                    fp.write(s)    
                QtCore.QThread.sleep(1)

        obj.SetSockTimeout(t0)
        




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #Form = MyRadialWidget(MyRadialWidget.SSL_VSERVER)
    Form = MyRectWidget(3)
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

