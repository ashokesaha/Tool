import sys
import os
import random
import httplib
import json
import socket
import numpy as np
import scipy as sp
from PyQt5 import QtCore, QtWidgets, QtGui

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.markers import MarkerStyle


class  AllocFreeForm (QtWidgets.QWidget):

    def ListCounters(self) :
        l = []
        for v in self.counterMap.values() :
            l.append(v[0])
            l.append(v[1])

        return l


    
    def  __init__(self, parent=None,plotwidth=0.3):
        
        super(self.__class__,self).__init__(parent)
        self.counterMap = dict()
        self.counterMap['BM16']  = ('sys_cur_alloc_bm16_entries','sys_cur_free_bm16_entries')
        self.counterMap['BM32']  = ('sys_cur_alloc_bm32_entries','sys_cur_free_bm32_entries')
        self.counterMap['BM64']  = ('sys_cur_alloc_bm64_entries','sys_cur_free_bm64_entries')
        self.counterMap['BM128'] = ('sys_cur_alloc_bm128_entries','sys_cur_free_bm128_entries')
        self.counterMap['BM256'] = ('sys_cur_alloc_bm256_entries','sys_cur_free_bm256_entries')
        self.counterMap['BM512'] = ('sys_cur_alloc_bm512_entries','sys_cur_free_bm512_entries')
        self.counterMap['SPCB']  = ('ssl_cur_sslInfo_SPCBAllocCount','ssl_cur_sslInfo_SPCBFreeCount')
        self.counterMap['PCB']   = ('pcb_cur_alloc', 'pcb_cur_free')
       

        self.axesmap = dict()
        self.plotwidth = plotwidth
        self.counterResult = None
        self.workerThread = None
        self.workerObj = None
        
        
        self.layout = QtWidgets.QHBoxLayout(self)
        self.fig = Figure(figsize=(3, 3), dpi=100)
        self.figCanvas = FigureCanvas(self.fig)
        self.fig.subplots_adjust(left=0.1, bottom=None, right=None, top=None,
                wspace=None, hspace=None)

        self.layout.addWidget(self.figCanvas)

        k = self.counterMap.keys()
        nc = 8
        nr = len(k)/nc
        if (len(k) % nc) :
            nr = nr + 1


        self.subplots = []
        for i in range(1,len(k)+1) :
            self.subplots.append(self.fig.add_subplot(nr,nc,i, frameon=True))
        
        for plt in self.subplots :
            plt.set_xticks([])
            plt.set_yticks([])
            plt.autoscale(tight=True)
            plt.set_facecolor('white')


        for k in self.counterMap.keys() :
            self.AddEntity(k)



    def AddEntity(self,name,useCount=0,freeCount=0) :
        try :
            found = 0
            for plt in self.subplots :
                if plt not in self.axesmap.values() :
                    self.axesmap[name] = plt
                    found = 1
                    break

            if not found:
                print 'no plots available'
                return -1

            p1 = plt.bar([0],[useCount], self.plotwidth)
            p2 = plt.bar([0],[freeCount],  self.plotwidth, bottom=[useCount])

            plt.text(0.0, useCount/2, str(useCount),
                             rotation='vertical',horizontalalignment='center',
                             verticalalignment='center')

            plt.text(0.0, useCount + freeCount/2, str(freeCount),
                             rotation='vertical',horizontalalignment='center',
                             verticalalignment='center')

            plt.autoscale(tight=True)
            plt.set_xlabel(name)

        except IndexError as e :
            print 'No available plots '
            return -1

    


    def RedrawEntity(self,name,useCount=0,freeCount=0) :
        try :
            plt = self.axesmap[name]
            plt.cla()

            plt.bar([0],[useCount], self.plotwidth)
            plt.bar([0],[freeCount],  self.plotwidth, bottom=[useCount])

            if ((useCount+freeCount) <= 0) :
                p1 = 0
                p2 = 100
            else :
                p1 = (float(useCount)/float(useCount+freeCount)) * 100
                p2 = 100 - p1
            
            if (p1 > 10) :
                if (p1 > 25) :
                    p1rot = 'vertical'
                else :
                    p1rot = 'horizontal'
                
                plt.text(0.0, useCount/2, str(useCount),
                             rotation=p1rot,horizontalalignment='center',
                             verticalalignment='center')

            if (p2 > 10) :
                if (p2 > 25) :
                    p2rot = 'vertical'
                else :
                    p2rot = 'horizontal'

                plt.text(0.0, useCount + freeCount/2, str(freeCount),
                             rotation=p2rot,horizontalalignment='center',
                             verticalalignment='center')

            plt.set_xticks([])
            plt.set_yticks([])
            plt.autoscale(tight=True)
            plt.set_xlabel(name)
 
        except KeyError as e :
            print 'No such entity as {}'.format(name)
            return -1


    def updateBar(self) :
        curylim = 0
        lastylim = 0
        
        for k in self.axesmap.keys() :
            v1 = np.random.randint(1,100)
            v2 = np.random.randint(1,100)
            curylim = self.RedrawEntity(k,v1,v2)
            if curylim > lastylim :
                lastylim = curylim

        self.figCanvas.draw()



    def UpdateResults(self, s) :
        D = json.loads(s)
        for k in self.counterMap.keys() :
            t = self.counterMap[k]
            v1 = D[t[0]]
            v2 = D[t[1]]
            self.RedrawEntity(k,v1-v2,v2)
    
        self.figCanvas.draw()
    




class  AllocFreeWorker(QtCore.QObject) :
    finished  = QtCore.pyqtSignal(int)
    results   = QtCore.pyqtSignal(str)
    
    def  __init__(self, parent=None,freq=7):
        super(self.__class__,self).__init__(parent)
        
        self.counterList = []
        self.nsip = None
        self.httpHandle = None
        self.dostop = False
        self.freq = freq


    def  AddCounters(self,cl) :
        for l in cl :
            self.counterList.append(l)
    
        
    def SetNSIP(self,nsip) :
        try :
            if self.httpHandle :
                self.httpHandle.close()
                self.httpHandle = None

            self.httpHandle = httplib.HTTPConnection(nsip,timeout=5.0)
            self.httpHandle.connect()
            self.nsip = nsip

        except socket.error as e :
            print 'Failed to set NSIP'
            self.nsip = None
            if self.httpHandle :
                self.HttpHandle.close()
                self.httpHandle = None



    def FetchCounters(self) :
        counterChunks = self.Chunkify(self.counterList,6)
        reqs = []
        D = dict()

        for clist in counterChunks :
            req = self.PrepareReq(clist)
            reqs.append(req)

        for req in reqs :
            doretry = 0
            try :
                self.SetNSIP(self.nsip)
                
                self.httpHandle.putrequest('GET',req)
                self.httpHandle.putheader('X-NITRO-USER','nsroot')
                self.httpHandle.putheader('X-NITRO-PASS','nsroot')
                self.httpHandle.endheaders()
                self.httpHandle.send('')

                resp = self.httpHandle.getresponse()
                d = resp.read()

            except httplib.BadStatusLine as e :
                print 'BadStatus: {}'.format(e.line)
            
            except socket.error as e :
                print 'socket exception happened..'
                doretry = 1
                self.SetNSIP(self.nsip)
                
                self.httpHandle.putrequest('GET',req)
                self.httpHandle.putheader('X-NITRO-USER','nsroot')
                self.httpHandle.putheader('X-NITRO-PASS','nsroot')
                self.httpHandle.endheaders()
                self.httpHandle.send('')
                resp = self.httpHandle.getresponse()
                d = resp.read()

            dd = json.loads(d)
            d = dd['nsglobalcntr']
            for k in d.keys() :
                D[str(k)] = int(d[k])

        self.counterResults = D
        s = json.dumps(D)
        return s



    def PrepareReq(self,clist) :
        Req = '/nitro/v1/stat/nsglobalcntr?args=counters:'
        s = ''
        for l in clist :
            s += l + ';'
        Req += s[:-1]
        return Req



    def Chunkify(self,cl,sz) :
        m = range(0,len(cl),sz)
        counterChunks = [self.counterList[x:x+sz] for x in m]
        return counterChunks




    def process(self) :
        while not self.dostop :
            print 'worker processing ...'
            s = self.FetchCounters()
            self.results.emit(s)
            i = 0
            while i < self.freq :
                if  self.dostop :
                    break
                QtCore.QThread.sleep(1)
                i += 1

            if self.dostop :
                break

        print 'dostop set for worker thread'
        QtCore.QThread.currentThread().exit(0)








class RateCounters(QtWidgets.QWidget) :
    def  __init__(self, parent=None,plotwidth=0.3):
        super(self.__class__,self).__init__(parent)
        self.freq = 7
        self.updateCount = 0
        self.counterMap = dict()
        self.counterMap['FETPS']  = ['ssl_tot_sslInfo_SSLv3HandskCount','ssl_tot_sslInfo_TLSv1HandskCount','ssl_tot_sslInfo_TLSv11HandskCount','ssl_tot_sslInfo_TLSv12HandskCount']
        self.counterMap['BETPS']  = ['ssl_tot_sslInfo_Backend_SSLv3HandskCount','ssl_tot_sslInfo_Backend_TLSv1HandskCount','ssl_tot_sslInfo_Backend_TLSv11HandskCount','ssl_tot_sslInfo_Backend_TLSv12HandskCount']
        self.xLabels = ('FETPS','BETPS')
            

        self.RateMap = dict()
        self.PrepareRateMap()

        self.axesmap = dict()
        self.plotwidth = plotwidth
        self.counterResult = None
        self.workerThread = None
        self.workerObj = None
            
            
        self.layout = QtWidgets.QHBoxLayout(self)
        self.fig = Figure(figsize=(3, 3), dpi=100)
        self.figCanvas = FigureCanvas(self.fig)
        self.fig.subplots_adjust(left=0.1, bottom=None, right=None, top=None,
                wspace=None, hspace=None)

        self.layout.addWidget(self.figCanvas)

        k = self.counterMap.keys()
        nc = 8
        nr = len(k)/nc
        if (len(k) % nc) :
            nr = nr + 1

        self.plt = self.fig.add_subplot(1,1,1,frameon=True)
        self.plt.autoscale(tight=True)
        self.plt.set_facecolor('white')
        self.plt.set_yticks(np.arange(0, 500, 100))
        self.plt.set_xticks(np.arange(len(self.xLabels)),self.xLabels)


    def ListCounters(self) :
        l = []
        for k in self.counterMap.keys() :
            for v in self.counterMap[k] :
                l.append(v)

        return l



    def PrepareRateMap(self) :
        for k in self.counterMap.keys()  :
            for v in self.counterMap[k] :
                self.RateMap[v] = [0,0]



    def UpdateResults(self, s) :
        print 'rate counter: UpdateResults triggered..'
        D = json.loads(s)
        for k in self.RateMap.keys() :
            l = self.RateMap[k]
            l[0] = l[1]
            l[1] = D[k]
            if not self.updateCount :
                l[0] = l[1]

        self.updateCount += 1
        self.RedrawEntity()
        self.figCanvas.draw()



    def RedrawEntity(self) :
        self.plt.cla()
        
        rr = []
        xLabels = self.xLabels
        ind = np.arange(0,1, 1.0/len(xLabels))
        a = [self.counterMap[x] for x in xLabels]
        ylen = max([len(x) for x in a])

                       
        for k in xLabels :
            r = []
            rr.append(r)
            for c in self.counterMap[k] :
                t = self.RateMap[c]
                r.append((t[1] - t[0])/self.freq)
                
        b = zip(*rr)
        btm = np.zeros(len(ind))
        z = np.zeros(len(ind))


        Plots = []
        for x in np.arange(len(b)) :
            plt = self.plt.bar(ind[:len(xLabels)], b[x], 0.1, bottom=btm[:len(xLabels)])
            Plots.append(plt)
            btm[:len(xLabels)] += b[x]
        print '\n'

        p1 = Plots[0]
        p2 = Plots[1]
        p3 = Plots[2]
        p4 = Plots[3]
        self.plt.legend((p1[0],p2[0],p3[0],p4[0]),('ssl3','tls1','tls11','tls12'), loc=9)

        
        self.plt.autoscale(tight=True)
        self.plt.set_xticks(ind)
        self.plt.set_xticklabels(xLabels)
        self.plt.set_yticks(np.arange(0,500,100))

            




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = AllocFreeForm(plotwidth=3)
    Form.show()

    W = AllocFreeWorker()
    W.SetNSIP('10.102.28.78')
    W.AddCounters(Form.ListCounters())
    T = QtCore.QThread()
    W.moveToThread(T)

    T.started.connect(W.process)
    W.finished.connect(T.quit)
    W.results.connect(Form.UpdateResults)
    
    T.start()
    
    sys.exit(app.exec_())


