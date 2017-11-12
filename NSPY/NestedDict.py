import sys
import json
from   PyQt5 import QtCore, QtGui, QtWidgets

class NestedDict(object) :
    
    def __init__(self) :
        self.keys = dict()
        self.keySeq = None
        self.myKey = None
        self.rowcount = 0
        self.colcount = 0
        self.tw = None
        self.addrow = 0
        

    def SetKeys(self, keyS) :
        self.keySeq = keyS
        self.colcount = len(keyS)
    

    def GetKeys(self) :
        return self.keySeq
    

    def AddDict(self,d) :
        D = self.keys
        self.rowcount += 1
        
        for k in self.keySeq :
            try :
                kk = None
                kk = d[k]
                D = D[kk]
            except KeyError as e :
                if not kk :
                    break
                D[kk] = dict()
                D = D[kk]

        try :
            if len(D.keys()) == 0 :
                D['success'] = 0
                D['failure'] = 0
            
            if cmp(d['result'],'Success') == 0 :
                D['success'] += 1
            else :
                D['failure'] += 1
        except KeyError as e :
            pass


    def AddItem(self,l) :
        rcount = self.addrow
        ccount = 0

        print 'AddItem : {}'.format(l)
        for ll in l :
            twi = QtWidgets.QTableWidgetItem(ll)
            self.tw.setItem(self.addrow,ccount,twi)
            ccount += 1
        
        self.addrow += 1



    def Print(self,d,l) :
        if 'success' in d.keys() :
            l.append(str(d['success']))
            l.append(str(d['failure']))
            print l
            self.AddItem(l)
            del l[-1]
            del l[-1]
            return

        kk = [k for k in d.keys()]
##        kk.append('success')
##        kk.append('failure')
        for k in  kk :
            l.append(k)
            self.Print(d[k],l)
            del l[-1]
        


    def LoadFile(self,filename) :
        with open(filename) as fp :
            for line in fp :
                d = json.loads(line)
                self.AddDict(d)


    def LoadFileFp(self,Fp) :
        for line in Fp :
            d = json.loads(line)
            print 'line {}'.format(line)
            print d
            self.AddDict(d)



    def GetViewWidget(self, dialog) :
        vHeaders = [h for h in self.GetKeys()]
        vHeaders.append('Success')
        vHeaders.append('Failure')
        
        self.tw = QtWidgets.QTableWidget(self.rowcount, self.colcount+2, dialog);
        self.tw.setHorizontalHeaderLabels(vHeaders)
        return self.tw




##N = NestedDict()
##K = ['version','cipher','ServerCert']
##N.SetKeys(K)
##
##fname = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\mylog.txt'
##with open(fname) as fp :
##    for line in fp :
##        print line
##        d = json.loads(line)
##        N.AddDict(d)
##
##l = []
##N.Print(N.keys,l)
##

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    N = NestedDict()
    K = ['version','cipher','ServerCert']
    N.SetKeys(K)
    N.LoadFile('C:\\Users\\ashokes\\Miniconda2\\PyLogs\\mylog.txt')
    tw = N.GetViewWidget()
    l = []
    N.Print(N.keys,l)
    tw.show()

    sys.exit(app.exec_())


