import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class  CounterWidget(QWidget) :
    def  __init__(self, parent=None):
        super(self.__class__,self).__init__(parent)
        qsz = QSize(100,100)
        self.setMinimumSize(qsz)
        qsz = QSize(200,200)
        self.setMaximumSize(qsz)
        self.values = []
        self.NUMTICKS = 10
        self.painterPath = QPainterPath()
        self.curTick = 0;
        self.R = None
        self.YSCALE = 10
        self.XSCALE = 4
        

    def sizeHint(self) :
        qsz = QSize(64,32)
        return qsz

    def paintEvent(self, event=None) :
        #print 'paintEvent : tick {}'.format(self.curTick)
        qP = QPainter(self)
        vw = qP.viewport()
        print 'paint : rect {} {} {} {}'.format(vw.x(),vw.y(),vw.width(),vw.height())
        qP.setRenderHint(QPainter.Antialiasing)
        qP.drawPath(self.painterPath)
    
        
        
    def AddValue(self,v) :
        self.values.append(v)
        h = self.rect().height()
        if len(self.values) == 0 :
            self.painterPath.moveTo(self.curTick * self.XSCALE, h - (v * self.YSCALE))
        else :
            self.painterPath.lineTo(self.curTick * self.XSCALE, h - (v * self.YSCALE))
        self.curTick += 1

        if self.isVisible() :
            #print 'AddValue: calling update()'
            self.update()
    

    def SetNumTicks(self,v) :
        self.NUMTICKS - v
        self.Recalibrate()
        self.update()


    def HideEvent(self,event) :
        print 'HideEvent'
        super(self.__class__,self).HideEevnt(event)

    
    

class  CounterWidgetThread(QThread) :
    sigInt = pyqtSignal(int)
    def __init__(self,wdgt) :
        super(self.__class__,self).__init__()
        self.wdgt = wdgt
        self.stopRunning = False
        self.L = [1,2,3,4,5,4,3,2,1,1,2,3,3,4,8,9,6,7,8,6,5,6,4,3,4,3,2.7,2.4,2.1,1.6,1.3,1.0,1.1,1.5,1.7,1.9,2.0,2.2,2.4]

    def StopRunning(self) :
        self.stopRunning = True

    def run(self) :
        for i in self.L :
            self.sigInt.emit(i)
            QThread.msleep(500)


        





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    W = CounterWidget()
    CT = CounterWidgetThread(W)
    CT.sigInt.connect(W.AddValue)
    CT.start()
    W.show()
    sys.exit(app.exec_())

