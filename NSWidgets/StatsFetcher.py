import os
import sys
import socket
import httplib
import json
from PyQt5 import QtCore, QtGui, QtWidgets


#####################################################################
#####################################################################

class StatsFetcher(QtCore.QThread) :
    sigdata = QtCore.pyqtSignal(int)

    def __init__(self,nsip,freq=5, maxCounters=10) :
        super(self.__class__,self).__init__()
        self.nsip = nsip
        self.freq = freq
        self.counterList = []
        self.maxCounters = maxCounters
        self.runInstance = 0
        self.threadRunning = False
        self.logFp = None
        self.Req = None
        self.h1 = None


    def AddCounter(self,countername) :
        if self.threadRunning :
            return False
        if len(self.counterList) >= self.maxCounters :
            return False
        self.counterList.append(countername)
        self.PrepareReq()
        return True


    def AddCounterList(self,l) :
        self.counterList = l
        self.PrepareReq()
        return True
  


    def CleanCounters(self) :
        self.counterList = None
        self.Req = None
    

    def Start(self) :
        ret = False
        if self.threadRunning :
            return ret

        fname = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\' + 'counter.' + str(self.runInstance) + '.log' 
        self.logFp = open(fname,'w')
        ret = True

        self.threadRunning = True
        self.start()
        self.runInstance += 1
        return ret


    def Stop(self) :
        self.threadRunning = False
        if self.logFp :
            self.logFp.close()


    def PrepareReq(self) :
        self.Req = '/nitro/v1/stat/nsglobalcntr?args=counters:'
        s = ''
        for l in self.counterList :
            s += l + ';'
        self.Req += s[:-1]
    

    def FetchOnce(self) :
        try :
            if not self.h1 :
                h1 = httplib.HTTPConnection(self.nsip,timeout=2.0)
                h1.connect()
                self.h1 = h1
            else :
                h1 = self.h1
            
            h1.putrequest('GET',self.Req)
            h1.putheader('X-NITRO-USER','nsroot')
            h1.putheader('X-NITRO-PASS','nsroot')
            h1.endheaders()
            h1.send('')
            h2 = h1.getresponse()
            d = h2.read()
            dd = json.loads(d)
            d = dd['nsglobalcntr']
            k = d.keys()
            k.sort()
            l = [d[x] for x in k]
            s =  ':'.join(l)
            return s
        except socket.error as e :
            return None
        except httplib.CannotSendRequest as e :
            print 'CannotSendRequest exception happened'
            h1 = httplib.HTTPConnection(self.nsip,timeout=2.0)
            h1.connect()
            self.h1 = h1
            return None
            
        

    def SetFreq(self,f) :
        self.freq = f
    


    def run(self) :
        icount = 0
        
        while  self.threadRunning :
            l = self.FetchOnce()
            if not l :
                break
            self.sigdata.emit(l)
            print 'StatsFetcher:run : writing to file'
            self.logFp.write(l + '\n')

            t = 0
            while t < self.freq :
                if not self.threadRunning :
                    break
                QtCore.QThread.sleep(1)
                t += 1
            if not self.threadRunning :
                break
            
            icount += 1
            if icount == 10 :
                break

    
    @QtCore.pyqtSlot()
    def RunFinish(self) :
        print 'RunFinish called'
        self.isRunning = False
        self.logFp.close()
        self.runThread = None
        self.stopThread = True


    @QtCore.pyqtSlot()
    def RunStart(self) :
        print 'RunStart called'






#####################################################################
#####################################################################
        
class FetcherThread(QtCore.QThread) :
    sigdata = QtCore.pyqtSignal(str)

    def __init__(self,nsip,freq=5, maxCounters=10) :
        super(self.__class__,self).__init__()
        self.nsip = nsip
        self.freq = freq
        self.counterList = []
        self.counterChunks = []
        self.doRun = False


    def SetFreq(self,f) :
        self.freq = f
    

    def AddCounters(self,counterList) :
        self.counterList = counterList


    def Chunkify(self,sz) :
        m = range(0,len(self.counterList),sz)
        self.counterChunks = [self.counterList[x:x+sz] for x in m]


    @QtCore.pyqtSlot()
    def DoStart(self) :
        t = self.doRun
        self.doRun = True
        if not t :
            self.start()
        
    
    @QtCore.pyqtSlot()
    def DoStop(self) :
        self.doRun = False


    def run(self) :
        fetcherList = []
        
        for cl in self.counterChunks :
            f = StatsFetcher(self.nsip)
            fetcherList.append(f)
            f.AddCounterList(cl)
          
        icount = self.freq
        
        while self.doRun :
            s = ''
            icount = self.freq
            
            for f in fetcherList :
                fs = f.FetchOnce()
                if not fs :
                    print 'FetchOnce failed .. Retrying..'
                    fs = f.FetchOnce()
                    if not fs :
                        print 'FetchOnce failed .. again..'
                        continue
                    print 'second attemp successful...'
                    continue
                #print 'FetchOnce got {}'.format(fs)
                s += fs + ':'

            #print 'FetcherThread:: emiting sigdata with {}'.format(s)
            self.sigdata.emit(s)
            
            while icount > 0 :
                if self.doRun :
                    QtCore.QThread.sleep(1)
                    icount -= 1
                else :
                    break

            if icount :
                break
        
        self.doRun = False        

    



#####################################################################
#####################################################################
class ThreadTestWidget(QtWidgets.QWidget) :

    def  __init__(self, parent=None):
        super(self.__class__,self).__init__(parent)
        qsz = QtCore.QSize(300,200)
        self.setMinimumSize(qsz)
        self.setMaximumSize(qsz)
        self.o = StatsFetcher('10.102.28.201')
        self.o.AddCounter('pcb_cur_alloc')
        self.o.AddCounter('ssl_cur_sslInfo_SPCBAllocCount')
        self.o.AddCounter('sys_cur_freensbs')
        self.o.started.connect(self.ThreadStarted)
        self.o.finished.connect(self.ThreadStopped)
        self.w = QtCore.QRect(0,0,300,200)

 
    def mousePressEvent(self,e) :
        x = self.w.x()
        y = self.w.y()
      
        b = e.button()
        if b == 1 :
            self.w.moveTo(x-5,y)
        if b == 2 :
            self.w.moveTo(x+5,y)

        self.update()
        return

        if self.o.threadRunning :
            self.o.Stop()
        else :
            self.o.Start()
    


    def ThreadStarted(self) :
        print 'ThreadStarted called'
    

    def ThreadStopped(self) :
        print 'ThreadStopped called'
        self.o.threadRunning = False
        self.o.logFp.close()


    def paintEvent(self, event=None) :
        points = [(0,30),(50,40),(100,100),(150,120),(180,110),(210,50),(250,80),(280,150),(310,20),(320,100),(330,50),(340,55),(350,58),(360,58)]
        qP = QtGui.QPainter(self)
        qP.setRenderHint(QtGui.QPainter.Antialiasing)
        qP.setWindow(self.w)
        w = self.w
        
        x = w.x()
        y = w.y()
        wd = w.width()
        ht = w.height()
        
        (x1,y1) = points[0]
        for (x2,y2) in points[1:] :
            qP.drawLine(x1,y1,x2,y2)
            x1 = x2
            y1 = y2
    
    






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = ThreadTestWidget()
    w.show()
    sys.exit(app.exec_())




