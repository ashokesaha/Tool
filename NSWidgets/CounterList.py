import os
import sys
import socket
import httplib
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from StatsFetcher import *

class NSCounterList :
    COUNTERS = ['ssl_tot_sslEvent_HandskFail',
                'ssl_tot_sslInfo_Backend_TLSv1HandskCount',
                'ssl_tot_sslInfo_Backend_SSLv3HandskCount',
                'ssl_tot_sslInfo_Backend_TLSv12HandskCount',
                'ssl_tot_sslInfo_SSLv3HandskCount',
                'ssl_tot_sslInfo_TLSv12HandskCount',
                'ssl_tot_sslInfo_TLSv1HandskCount',
                'ssl_cur_nsb_in_handshakeQ',
                'ssl_cur_nsb_in_recordQ',
                'ssl_cur_sslInfo_cardinBlkQ',
                'ssl_cur_sslInfo_SPCBInUseCount',
                'ssl_cur_sslInfo_SPCBAllocCount',
                'ssl_cur_sslInfo_SessionNodeAllocCount',
                'ssl_cur_sslInfo_SessionNodeFreeCount',
                'pcb_cur_inuse',
                'sys_cur_alloc_bm64_entries']


    CHNKS = []

    DICT = dict()

    COLORS = []
    nextColor = 0

    @classmethod
    def  Init(cls) :
        NSCounterList.COUNTERS.sort()
        for c in NSCounterList.COUNTERS :
            NSCounterList.DICT[c] = NSCounterList.COUNTERS.index(c)

        NSCounterList.Chunkify(5)

        NSCounterList.COLORS.append(QtGui.QColor(80,80,80,100))
        NSCounterList.COLORS.append(QtGui.QColor(20,20,20,200))
        NSCounterList.COLORS.append(QtGui.QColor(100,0,0,150))
        NSCounterList.COLORS.append(QtGui.QColor(0,100,0,150))
        NSCounterList.COLORS.append(QtGui.QColor(0,0,100,150))
        NSCounterList.COLORS.append(QtGui.QColor(100,100,0,250))
        NSCounterList.COLORS.append(QtGui.QColor(100,0,100,250))
        NSCounterList.COLORS.append(QtGui.QColor(0,100,100,250))
        NSCounterList.COLORS.append(QtGui.QColor(100,100,0,250))
        NSCounterList.COLORS.append(QtGui.QColor(50,100,50,250))
        NSCounterList.COLORS.append(QtGui.QColor(100,50,50,250))
        NSCounterList.COLORS.append(QtGui.QColor(50,50,100,250))



    @classmethod
    def Chunkify(cls,sz) :
        m = range(0,len(NSCounterList.COUNTERS),sz)
        NSCounterList.CHNKS = [NSCounterList.COUNTERS[x:x+sz] for x in m]
        


    @classmethod
    def GetNextColor(cls) :
        NSCounterList.nextColor += 1
        if (NSCounterList.nextColor >= len(NSCounterList.COLORS)) :
            NSCounterList.nextColor = 0
        return NSCounterList.COLORS[NSCounterList.nextColor]



    @classmethod
    def CounterIndex(cls,name) :
        idx = NSCounterList.DICT[name]
        #print 'CounterIndex : {} {}'.format(name,idx)
        return idx




#########################################################################
#########################################################################
class NSCounter (object) :
    def __init__(self,name) :
        self.name = name
        self.YSCALE = 1.0
        self.XSCALE = 1.0
        self.HEIGHT = 0
        self.WIDTH = 0
        self.fromTick = 0
        self.toTick = 0
        self.lastTick = 0
        self.values = []
        self.color = None
        self.path = None


    def Init(self,xscale,yscale,height,width,fromtick,totick,color) :
        if xscale :
            self.XSCALE = xscale
        if yscale :
            self.YSCALE = yscale
        if height :
            self.HEIGHT = height
        if width :
            self.WIDTH =  width
        if fromtick :
            self.fromTick = fromtick
        if totick :
            self.toTick = totick
        if color :
            self.color = color
    

    def MakePath(self) :
        if self.path :
            self.path = None

        tick = self.fromTick
        for v in self.values :
            if tick > self.toTick :
                break
            x = tick * self.XSCALE
            y = self.HEIGHT - v * self.YSCALE
            pt = QtCore.QPointF(x,y)
            
            if not self.path :
                self.path = QtGui.QPainterPath(pt)
            else :
                self.path.lineTo(pt)

        self.lastTick = tick
        return self.path


    def CheckYScale(self,v) :
##        if v > 0 :
##            print 'CheckYScale:: {} {}'.format(float(self.HEIGHT/v), float(self.HEIGHT/v) / 1.1)
        if (self.HEIGHT - v * self.YSCALE) < 0 :
            yscale = float(self.HEIGHT/v) / 1.1
        else :
            yscale = float(self.YSCALE)
        return yscale


    def AddOnePoint(self,v) :
        print '{} -> {}'.format(self.name,v)
        self.values.append(v)
        x = self.lastTick * self.XSCALE
        y = self.HEIGHT - v * self.YSCALE
        pt = QtCore.QPointF(x,y)
        print 'adding point {} {}'.format(x,y)
        if not self.path :
            self.path = QtGui.QPainterPath(pt)
        else :
            self.path.lineTo(pt)
        self.lastTick += 1
    


    def RePath(self) :
        values = self.values
        self.values = []
        self.path = None
        self.lastTick = 0

        for v in values :
            self.AddOnePoint(v)

      



#######################################################################
#######################################################################
        
class NSCounterHarnessWidget(QtWidgets.QWidget) :
    startFetcher = QtCore.pyqtSignal()
    stopFetcher  = QtCore.pyqtSignal()
    
    def __init__(self,parent=None) :
        super(self.__class__,self).__init__(parent)
        self.fetcherThread  = None
        self.counterList    = []
        self.fromTick       = 0.0
        self.toTick         = 0.0
        self.lastTick       = 0.0
        self.fromDispTick   = 0.0
        self.XSCALE         = 1.0
        self.YSCALE         = 1.0
        self.WIDTH          = 300.0
        self.HEIGHT         = 200.0
        self.w              = QtCore.QRect(0,0,300.0,200.0)
        self.fetcherRun     = False
        self.toTick         = int(self.WIDTH/self.XSCALE)

        self.mmInProgress   = False
        self.mmLastX        = 0

        self.setStyleSheet("background-color: rgb(100, 100, 100);")
        
        qsz = QtCore.QSize(self.WIDTH, self.HEIGHT)
        self.setMinimumSize(qsz)
        qsz = QtCore.QSize(10000, 1000)
        self.setMaximumSize(qsz)




    def SideShiftWindow(self, ticks) :
        print 'SideShiftWindow ({},{},{}'.format(self.fromTick,self.toTick,self.lastTick)
        dx = ticks * self.XSCALE
        self.w.adjust(dx,0,dx,0)
        self.fromTick += ticks
        self.toTick  += ticks

        

    def AddCounter(self,cname) :
        c = NSCounter(cname)
        c.Init(self.XSCALE,self.YSCALE,self.HEIGHT,self.WIDTH,self.fromTick,self.toTick,NSCounterList.GetNextColor())
        self.counterList.append(c)


    def SetXYScale(self,xs,ys) :
        print 'widget SetXYScale {} {}'.format(xs,ys)
        if not xs :
            xs = self.XSCALE
        else :
            self.XSCALE = xs
            self.toTick = self.fromTick + (self.WIDTH/self.XSCALE)

            
        if not ys :
            ys = self.YSCALE
        else :
            self.YSCALE = ys
            
        for c in self.counterList :
            c.Init(xs,ys,None,None,None,None,None)



    def RePath(self) :
        for c in self.counterList :
            c.RePath()
        

    def SetFromToTicks(self,fromTick,toTick) :
        for c in self.counterList :
            c.Init(None,None,None,None,fromTick,toTick,None)
        
 

    def AddOneTick(self,valstr) :
        print '\n'
        print 'AddOneTick ({},{},{}'.format(self.fromTick,self.toTick,self.lastTick)
        
        l = valstr.split(':')
        del l[-1]
        li = [int(i) for i in l]

        yscale = self.YSCALE
        for c in self.counterList :
            idx = NSCounterList.CounterIndex(c.name)
            tscale = c.CheckYScale(li[idx])
            if tscale < yscale :
                yscale = tscale

        #print 'yscale {}  self.YSCALE {}'.format(yscale,self.YSCALE)
        if yscale < self.YSCALE :
            self.YSCALE = yscale
            self.SetXYScale(self.XSCALE,self.YSCALE)
            self.RePath()


        for c in self.counterList :
            idx = NSCounterList.CounterIndex(c.name)
            c.AddOnePoint(li[idx])
        
##        x = (self.lastTick - 1) * self.XSCALE
##        y = 0
##        w = self.XSCALE * 2
##        h = self.HEIGHT
##        self.update(x,y,w,h)
##        print 'Updating {} {} {} {}'.format(x,y,w,h)

        if not self.mmInProgress :
            # In case of mouse move, update would be called from there
            self.update()
            
        self.lastTick += 1

        if (self.toTick - self.lastTick) <= 1 :
            self.SideShiftWindow(10)
        


    def SetFetcherThread(self,f) :
        self.fetcherThread = f
        f.sigdata[str].connect(self.FetcherSlot)
        self.startFetcher.connect(f.DoStart)
        self.stopFetcher.connect(f.DoStop)


    def mouseMoveEvent(self, e) :
        print 'mouseMoveEvent ... {} {}'.format(e.pos().x(),e.pos().y())
        x = e.pos().x()
        if x <= 0 :
            self.HandleMoveBreak()
        
        if not self.mmInProgress :
            self.mmLastX = x
            self.mmInProgress = True
        elif (x < self.mmLastX ) :
            self.HandleMoveBreak()
        else :
            xx = x - self.mmLastX
            if xx > self.XSCALE :
                self.mmLastX = xx
                self.w.adjust(-xx,0,-xx,0)
                self.update()
            


    def HandleMoveBreak(self) :
        self.mmLastX = 0
        self.mmInProgress = False
       
            
    
    def mouseReleaseEvent(self,e) :
        print 'mouseReleaseEvent.. called'
        self.HandleMoveBreak()
    

    def paintEvent(self, event=None) :
        qP = QtGui.QPainter(self)
        qP.setRenderHint(QtGui.QPainter.Antialiasing)
        qP.setWindow(self.w)

        br = QtGui.QBrush(QtGui.QColor(0,100,100,150))
        qP.setBrush(br)
        qP.drawRect(self.rect())

        for c in self.counterList :
            if c.path :
                qP.setPen(c.color)
                qP.drawPath(c.path)



    def contextMenuEvent(self, event) :
        print 'contextMenuEvent of  counter list'
        menu = QtWidgets.QMenu(self)
        
        FetcherStartAct = FetcherStopAct = None
        
        if self.fetcherRun :
            FetcherStopAct  = menu.addAction('Fetcher Stop')
        else :
            FetcherStartAct = menu.addAction('Fetcher Start')

        act = menu.exec_(event.globalPos())
        if act == FetcherStartAct :
            self.fetcherRun = True
            self.FetcherStart()
        elif act == FetcherStopAct:
            self.fetcherRun = False
            self.FetcherStop()
    



    @QtCore.pyqtSlot(str)
    def FetcherSlot(self,s) :
        self.AddOneTick(s)
    

    def FetcherStop(self) :
        self.stopFetcher.emit()
    

    def FetcherStart(self) :
        self.startFetcher.emit()
    
    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NSCounterList.Init()

    F = FetcherThread('10.102.28.201')
    F.AddCounters(NSCounterList.COUNTERS)
    F.Chunkify(5)
    
    w = NSCounterHarnessWidget()
    w.SetFetcherThread(F)
    w.AddCounter('ssl_cur_sslInfo_SPCBInUseCount')
    w.AddCounter('ssl_tot_sslInfo_TLSv1HandskCount')
    w.SetXYScale(5.0,0.1)
    w.SetFromToTicks(0,100)

    w.show()
    sys.exit(app.exec_())
