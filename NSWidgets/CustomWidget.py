# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CustomWidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import os
from   PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from   BEOpenSSLServerDialog import *
from   ocsp_responder import *
import DUTDialog
from   TestTemplateOne  import *
import BasicClientDialog
import SSLVServerDialog
import HttpVServerDialog
import SSLServiceDialog
import CertInstaller
import test_util
import ResultDialog
import NestedDict
import GenericContainer as GC
import nssrc.com.citrix.netscaler.nitro.resource.config.ns.nshardware as NSHW
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcipher_binding as SSLVSRVRCIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslciphersuite_binding as SSLVSRVRCIPHERSUITE


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(100, 100)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))




class  MyRectWidget(QtWidgets.QWidget) :

    INSTANCE_COUNT = 0
    
    def  __init__(self, typ, ccode, parent=None):
        super(self.__class__,self).__init__(parent)
        MyRectWidget.INSTANCE_COUNT += 1
        self.instanceId = MyRectWidget.INSTANCE_COUNT
        self.type = typ
        self.container = None
        self.parent = parent

        if not ccode :
            self.ccode = 0
        else :
            self.ccode = ccode

        if (self.type != GenericContainer.GenericContainer.CONTAINER_NSHOLDER and
            self.type != GenericContainer.GenericContainer.CONTAINER_NS) :
            qsz = QtCore.QSize(80,60)
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

        self.setAcceptDrops(True)
        
        self.backend_obj = None
        self.up = 0
        self.Th = None


    def SetContainer(self,w) :
        self.container = w


    def GetType(self) :
        return self.type


    def GetCurDUT(self) :
        return self.container.GetCurDUT()


    def SetCurDUT(self,dut) :
        self.container.SetCurDUT(dut)        

    def AddDUT(self,dut) :
        self.container.AddDUT(dut)


    def sizeHint(self) :
        qsz = QtCore.QSize(64,32)
        return qsz



    def slotStatus(self, status) :
        self.update()


    def mousePressEvent(self,e) :
        if e.button() == QtCore.Qt.LeftButton :
            if not self.GetBackendObj() :
                self.dragStart = 0
                return
            self.dragStart = e.pos()


    def mouseMoveEvent(self,e) :
        if  not (e.buttons() & QtCore.Qt.LeftButton) :
            return
        if (e.pos() - self.dragStart).manhattanLength() < 8 :
            return
        o = self.GetBackendObj()
        if not o :
            return
        pmap = QtGui.QPixmap('C:\Users\ashokes\Miniconda2\mypixmap.png', format='PNG')
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        s = o.PrepareMimeData(self.ccode)
        mimeData.setText(s)
        drag.setMimeData(mimeData)
        drag.setPixmap(pmap)
        d = drag.exec_(QtCore.Qt.CopyAction |QtCore.Qt.MoveAction )




    def dragEnterEvent(self,e) :
        t = e.mimeData().text()
        d = json.loads(t)
        typ = d['type']
        o = self.GetBackendObj()
        if not o :
            return
        if o.entity_type == typ :
            return
        if o.AllowDrop(t) :
            e.acceptProposedAction()


    def dropEvent(self,e) :
        o = self.GetBackendObj()
        if not o :
            return
        t = e.mimeData().text()
        d = json.loads(t)
        if d['ccode'] :
            self.ccode = d['ccode']
        
        o.HandleDropEvent(t)
        self.update()



    def contextMenuEvent(self, event) :
        if self.type == GenericContainer.GenericContainer.CONTAINER_NSHOLDER :
            return

        if self.type == GenericContainer.GenericContainer.CONTAINER_NS :
            return NSWidgetContextMenu(self,event)
        
        menu    = QtWidgets.QMenu(self)
        stopAct = startAct = delAct = resAct = None
        obj     = self.GetBackendObj()
        
        if obj and obj.IsStartStop():
            if obj.isrunning :
                stopAct = menu.addAction('Stop')
            else :
                startAct = menu.addAction('Start')
                delAct   = menu.addAction('Delete')
 
        if obj and obj.IsProperty():
            propAct   = menu.addAction('Properties')

        if obj and obj.IsResults():
            resAct   = menu.addAction('Results')


        act = menu.exec_(event.globalPos())

        if act == startAct :
            obj.Start()
        
        elif act == stopAct :
            obj.Stop()
            if self.Th :
                self.Th.StopRunning()
                self.Th = None
            
        elif (act == delAct) :
            pass

        elif (act == resAct) :
            dialog = QtWidgets.QDialog()
            w = ResultDialog.ResultDialog(self)
            w.setupUi(dialog)
            dialog.exec_()
            
        elif (act == propAct) :
            dialog = QtWidgets.QDialog()
            
            if (self.type == GenericContainer.GenericContainer.TYPE_BE_OPENSSL_SERVER) :
                w = BEOpenSSLServerDialog(self)
            elif (self.type == GenericContainer.GenericContainer.TYPE_FE_OPENSSL_CLIENT) :
                w = BasicClientDialog.BasicClientDialog(self)
            elif (self.type == GenericContainer.GenericContainer.TYPE_OCSP_OPENSSL_SERVER) :
                w = OcspResponderDialog(self)
            elif (self.type == GenericContainer.GenericContainer.TYPE_SSL_VSERVER) :
                w = SSLVServerDialog.SSLVServerDialog(self)
            elif (self.type == GenericContainer.GenericContainer.TYPE_HTTP_VSERVER) :
                w = HttpVServerDialog.HttpVServerDialog(self)
            elif (self.type == GenericContainer.GenericContainer.TYPE_SSL_SERVICE) :
                w = SSLServiceDialog.SSLServiceDialog(self)

        
            w.setupUi(dialog)
            dialog.exec_()


    def GetInstanceId(self) :
        return self.instanceId



    def paintEvent(self, event=None) :
        if self.up :
            self.UpPaintEvent(event)
        else :
            self.DownPaintEvent(event)

        o = self.GetBackendObj()
        if not o :
            return
        
        name = o.GetName()

        if o.IsRunning() :
            pen = QtGui.QPen(QtGui.QColor(200,200,200,255))
        else :
            pen = QtGui.QPen(QtGui.QColor(20,20,20,255))
        
        pen.setWidth(8)
        qP = QtGui.QPainter(self)
        qP.setPen(pen)
        r = self.rect()
        qP.drawText(r,QtCore.Qt.AlignCenter,name)

    

    def SetUp(self) :
        self.up = 1
        self.repaint(self.rect())


    def SetDown(self) :
        self.up = 0
        self.repaint(self.rect())
        


    def DownPaintEvent(self, event=None) :
        o = self.GetBackendObj()
        if o and o.IsRunning() :
            alpha = 250
        else :
            alpha = 150

        gd = QtGui.QLinearGradient(0,0,self.width(),self.height())
        gd.setStart(0,0)
        gd.setFinalStop(self.width()*3/4, self.height()*3/4)
        gd.setSpread(1)

        try :
            if self.type == GenericContainer.GenericContainer.CONTAINER_NS :
                c1 = GenericContainer.GenericContainer.colorMap[self.type]
                c2 = c1
            elif self.type == GenericContainer.GenericContainer.CONTAINER_NSHOLDER :
                c1 = GenericContainer.GenericContainer.colorMap[self.type]
                c2 = c1
            else :
                c = GenericContainer.GenericContainer.FrontBackColor[self.ccode][0]
                c1 = QtGui.QColor(c)
                c1.setAlpha(alpha)
                c2 = c1

        except TypeError as e :
            print 'Error : entity type {}  ccode {}'.format(self.type, self.ccode)
            print e.message
        

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

        qP.setPen(QtCore.Qt.NoPen)
        qP.setRenderHint(QtGui.QPainter.Antialiasing)

        brush = QtGui.QBrush(gd)
        qP.setBrush(brush)
        r = self.rect()
        qP.drawRect(2,2,r.width()-6,r.height()-6)



    def SetBackendObj(self,obj) :
        self.backend_obj = obj
    

    def GetBackendObj(self) :
        return self.backend_obj


    def CheckMyThread(sel) :
        th = QtCore.QThread.currentThreadId()


    def GetDUTByIP(self,nsip) :
        return self.container.GetDUTByIP(nsip)


    
    def __del__(self) :
        print 'entity widget destroyed {}'.format(self)







class NSWidget(QtWidgets.QWidget) :
    def  __init__(self,parent=None,ccode=0):
        super(self.__class__,self).__init__(parent)
        self.type = GenericContainer.GenericContainer.CONTAINER_NS
        self.backend_obj = None
        self.up = 0
        self.container = None
        self.hardware = None
        self.isActive = None
        self.ccode = ccode


    def GetHardware(self) :
        dut = self.GetCurDUT()
        hw = NSHW.nshardware.get(dut.sess)
        

    def SetContainer(self,w) :
        self.container = w


    def paintEvent(self, event=None) :
        c1 = GenericContainer.GenericContainer.FrontBackColor[self.ccode][0]
        c2 = c1.lighter(75)
        c2 = c1


        gd = QtGui.QLinearGradient(0,0,self.width(),self.height())
        gd.setStart(0,0)
        gd.setFinalStop(self.width()*3/4, self.height()*3/4)
        gd.setSpread(1)

        gd.setColorAt(0,c1)
        gd.setColorAt(1,c2)

        qP = QtGui.QPainter(self)
        qP.setPen(QtCore.Qt.NoPen)
        qP.setRenderHint(QtGui.QPainter.Antialiasing)

        brush = QtGui.QBrush(gd)
        qP.setBrush(brush)
        qP.drawRect(self.rect())

        if self.backend_obj :
            textLabel = None
            textLabel = self.backend_obj.nsip + '\n' + '(' + self.backend_obj.hwdescription + ')'

            pencolor = GenericContainer.GenericContainer.FrontBackColor[self.ccode][1]
            pencolor = QtGui.QColor(pencolor)
            aF = pencolor.alpha()
            if self.isActive :
                pencolor.setAlpha(aF + 100)
            else :
                pass
                
            pen = QtGui.QPen(pencolor)
            
            qF = qP.font()
            qF.setPixelSize(18)
            qP.setFont(qF)
            qP.setPen(pen)
            r = self.rect()
            qP.drawText(r,QtCore.Qt.AlignCenter,textLabel)
 


    def contextMenuEvent(self, event) :
        bo = self.GetBackendObj()
        if bo and bo.IsRunning() :
            return
        
        menu = QtWidgets.QMenu(self)
        actionList = []

        typeS = GenericContainer.GenericContainer.typeMap[self.type]
        if self.backend_obj :
            for t in typeS :
                name = GenericContainer.GenericContainer.nameMap[t]
                act = menu.addAction(name)
                qv = QtCore.QVariant(t)
                act.setData(qv)
                actionList.append(act)
        else :
            name = GenericContainer.GenericContainer.nameMap[typeS[0]]
            act = menu.addAction(name)
            qv = QtCore.QVariant(typeS[0])
            act.setData(qv)
            actionList.append(act)

            

        act = menu.exec_(event.globalPos())
        w = None
        
        if act :
            t = act.data()
            dialog = QtWidgets.QDialog()
            dialog.setModal(True)
            
            if t == GenericContainer.GenericContainer.TYPE_NS_SELECT_DUT :
                w = DUTDialog.DUTDialog(self)

            elif t == GenericContainer.GenericContainer.TYPE_NS_INSTALL_CERT :
                obj = self.GetBackendObj()
                dut = self.GetCurDUT()
                
                if not obj :
                    print 'No NS attached'
                    return
                if not obj.sess :
                    print 'No session with NS'
                    return
                ci = CertInstaller.CertInstall()
                ci.SetCertDir('C:\\Users\\ashokes\\Miniconda2\\NSPY\\Certs')

                ci.PushToNS(obj.nsip)
                obj.Login()
                ci.Link(obj.sess)
                test_util.AddTCPMonitor(obj.sess,'quick_mon')
                dut.FillCerts()

            elif t == GenericContainer.GenericContainer.TYPE_NS_CLEAR_CONFIG :
                obj = self.GetBackendObj()
                if not obj :
                    return
                obj.Login()
                obj.sess.clear_config(level='basic')
                dut = self.GetCurDUT()
                dut.FillCerts()

            elif t == GenericContainer.GenericContainer.TYPE_TEST_TMPLT_ONE :
                obj = self.GetBackendObj()
                if not obj :
                    return

                dut = self.GetCurDUT()
                tt = TestTemplateOne('tone', obj.GetSess(), self.container)
                tt.Apply()

            if w :
                w.setupUi(dialog)
                dialog.exec_()


    def SetBackendObj(self,obj) :
        self.backend_obj = obj
    

    def GetBackendObj(self) :
        return self.backend_obj


    def GetCurDUT(self) :
        return self.container.GetCurDUT()


    def SetCurDUT(self) :
        self.container.SetCurDUT(self.GetBackendObj())        

    def AddDUT(self,dut) :
        self.container.AddDUT(dut)


    def mouseDoubleClickEvent(self,e) :
        self.SetCurDUT()        





class  CustomWidgetThread(QtCore.QThread) :
    def __init__(self,wdgt) :
        super(self.__class__,self).__init__()
        self.sigStr = QtCore.pyqtSignal(str)
        self.sigIntList = QtCore.pyqtSignal([])
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
        fname = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\' + obj.name + '_' + str(thid) + '.log'

        t0 = obj.GetSockTimeout()
        obj.SetSockTimeout(0.2)
        
        with open(fname,'a') as fp  :
            while not self.stopRunning :
                s = obj.ReadOnce()
                if s :
                    fp.write(s)    
                QtCore.QThread.sleep(1)

        obj.SetSockTimeout(t0)
        





class LogReaderThreadX(QtCore.QThread) :
    
    def __init__(self) :
        super(self.__class__,self).__init__()
        self.objList = []
        self.sleeptime = 1.0


    def RegisterObj(self, obj) :
        obj.isRemoved = False
        self.objList.append(obj)


    def RemoveObj(self, obj) :
        if obj in self.objList :
            self.objList.remove(obj)
        obj.isRemoved = True


    def SetSleepTime(self, t) :
        self.sleeptime = float(t)


    def run(self) :
        while True :
            for o in self.objList :
                if not o.IsRunning() :
                    self.RemoveObj(o)
                    while not o.isRemoved :
                        QtCore.QThread.sleep(0.25)
                    continue
                t = o.GetSockTimeout()
                o.SetSockTimeout(0.1)
                s = o.ReadOnce()
                o.SetSockTimeout(t)

            QtCore.QThread.sleep(1)

    




class ListWidgetDD(QtWidgets.QListWidget) :
    TYPE_CERT = 0X01
    TYPE_CIPHER = 0X10
    TYPE_CIPHERSUITE = 0X20

    cipherAdded   = QtCore.pyqtSignal(str)
    cipherDeleted = QtCore.pyqtSignal(str)
    certAdded   = QtCore.pyqtSignal(str)
    certDeleted = QtCore.pyqtSignal(str)

    
    def __init__(self,maxe,parent,type = None) :
        self.certList = []
        self.maxe = maxe
        self.type = type
        super(ListWidgetDD, self).__init__(parent)



    def AddToList(self, s) :
        if not s :
            return
        if len(s) == 0 :
            return
        self.certList.append(s)
        QtWidgets.QListWidgetItem(s,self)


    def AddCipherToList(self, s) :
        if not s :
            return
        if len(s) == 0 :
            return
        QtWidgets.QListWidgetItem(s,self)
        self.cipherAdded.emit(s)


    def contextMenuEvent(self, event) :
        menu = QtWidgets.QMenu(self)
        actD = menu.addAction('Delete')
        act = menu.exec_(event.globalPos())
        if act == actD :
            r = self.currentRow()
            s = self.item(r).text()
            self.cipherDeleted.emit(s)
            self.takeItem(r)
            self.certDeleted.emit(s)
            self.certList.remove(s)




    def dragEnterEvent(self,e) :
        if self.maxe > 0 :
            if self.count() >= self.maxe :
                return
        md = e.mimeData()
        mdata = md.data('application/x-qabstractitemmodeldatalist')
        data = self.decode_data(mdata)
        if data in self.certList :
            return
        super(ListWidgetDD, self).dragEnterEvent(e)



    def dropMimeData(self,index,data,action) :
        ret = super(ListWidgetDD, self).dropMimeData(index,data,action)
        i = self.item(index)
        self.cipherAdded.emit(i.text())
        self.certList.append(i.text())
        self.certAdded.emit(i.text())
        return ret


        


    def decode_data(self, mdata):
        data = []
        item = {}
        
        ds = QtCore.QDataStream(mdata)
        while not ds.atEnd():
            row = ds.readInt32()
            column = ds.readInt32()
            
            map_items = ds.readInt32()
            for i in range(map_items):
                key = ds.readInt32()
                value = QtCore.QVariant()
                ds >> value
                item[QtCore.Qt.ItemDataRole(key)] = value
            
            data.append(item)
        return data[0][0].value()





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #Form = MyRadialWidget(MyRadialWidget.SSL_VSERVER)
    Form = MyRectWidget(3)
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())




##class  MyRadialWidget(QtWidgets.QWidget)  :
##
##    SSL_VSERVER         = 1
##    SSL_TCP_vserver     = 2
##    HTTP_VSERVER        = 3
##    SSL_SERVICE         = 4
##    SSL_TCP_SERVICE     = 5
##    HTTP_SERVICE        = 6
##        
##    
##    def  __init__(self, type, parent=None):
##        super(self.__class__,self).__init__(parent)
##        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
##        self.setStyleSheet("background:transparent;")
##        self.colorList = []
##        self.a = None
##        self.setColors()
##        if ((type < MyRadialWidget.SSL_VSERVER) or (type > MyRadialWidget.HTTP_SERVICE)) :
##            type = MyRadialWidget.SSL_VSERVER
##            
##        self.entity_color = self.getEntityColor(type)
##        self.bgcolor = QtGui.QColor(0,0,0,0)
##        self.bgbrush = QtGui.QBrush(self.bgcolor, QtCore.Qt.SolidPattern)
##
##        qsz = QtCore.QSize(32,32)
##        self.setMinimumSize(qsz)
##        self.setMaximumSize(qsz)
##
##
##    def mousePressEvent(self,event) :
##        x  = event.x()
##        y  = event.y()
##
##        x -= self.a/2
##        y -= self.b/2
##        a  = float(self.a)/2
##        b  = float(self.b)/2
##        
##        r1 =  float(x * x)/float(a * a)
##        r2 =  float(y * y)/float(b * b)
##        r  = r1 + r2
##        if(r < 1.0) :
##            self.handleMousePress(event)
##
##
##    def  handleMousePress(self,event) :
##        pass
##
##    def  getEntityColor(self,type) :
##        for ec in self.colorList :
##            if ec.type == type :
##                return ec
##        return None
##
##
##    def  paintEvent(self, event=None) :
##        r  = self.rect()
##        h  = r.height()
##        w  = r.width()
##
##        qP = QtGui.QPainter(self)
##        qP.setPen(QtCore.Qt.NoPen)
##        qP.setRenderHint(QtGui.QPainter.Antialiasing)
##
##        qP.setBrush(self.bgbrush)
##        qP.drawRect(r)
##        
##        if((w - 4) > (h - 4)) :
##            self.a = h - 4
##        else :
##            self.a = w - 4
##
##        gd = QtGui.QRadialGradient(2+self.a/2, 2+self.a/2, self.a/2)
##        gd.setColorAt(0,self.entity_color.c2)
##        gd.setColorAt(1,self.entity_color.c1)
##        self.brush = QtGui.QBrush(gd)
##        qP.setBrush(self.brush)
##        qP.drawEllipse(2,2,self.a,self.a)
##
##
##    def  setColors(self) :
##        c1 = QtGui.QColor(50,0,0,250)
##        c2 = QtGui.QColor(200,0,0,250)
##        c  = EntityColor(1,c1,c2)
##        self.colorList.append(c)
##
##        c1 = QtGui.QColor(0,50,0,250)
##        c2 = QtGui.QColor(0,0200,0,250)
##        c  = EntityColor(2,c1,c2)
##        self.colorList.append(c)
##
##        c1 = QtGui.QColor(0,0,50,250)
##        c2 = QtGui.QColor(0,0,200,250)
##        c  = EntityColor(3,c1,c2)
##        self.colorList.append(c)
##
##        c1 = QtGui.QColor(50,50,50,250)
##        c2 = QtGui.QColor(200,200,200,250)
##        c  = EntityColor(4,c1,c2)
##        self.colorList.append(c)
##
##        c1 = QtGui.QColor(50,10,10,250)
##        c2 = QtGui.QColor(200,40,40,250)
##        c  = EntityColor(5,c1,c2)
##        self.colorList.append(c)
##
##        c1 = QtGui.QColor(0,50,50,250)
##        c2 = QtGui.QColor(0,200,200,250)
##        c  = EntityColor(6,c1,c2)
##        self.colorList.append(c)
##
##        c1 = QtGui.QColor(30,50,0,250)
##        c2 = QtGui.QColor(120,200,0,250)
##        c  = EntityColor(7,c1,c2)
##        self.colorList.append(c)
##
##        c1 = QtGui.QColor(50,0,50,250)
##        c2 = QtGui.QColor(200,0,200,250)
##        c  = EntityColor(8,c1,c2)
##        self.colorList.append(c)
##
##        c1 = QtGui.QColor(50,90,50,250)
##        c2 = QtGui.QColor(200,240,200,250)
##        c  = EntityColor(9,c1,c2)
##        self.colorList.append(c)
##
##        
##    def sizeHint(self) :
##        qsz = QtCore.QSize(32,32)
##        return qsz
##
##
##class  EntityColor() :
##    def  __init__(self, type, c1, c2) :
##        self.type = type
##        self.c1 = c1
##        self.c2 = c2
##


