import sys
import json

class NestedDict(object) :
    def __init__(self) :
        self.keys = dict()
        self.keySeq = None
        self.myKey = None

    def SetKeys(self, keyS) :
        self.keySeq = keyS

    def GetKeys(self) :
        return self.keys.keys()
    

    def AddDict(self,d) :
        D = self.keys

        for k in self.keySeq :
            #print 'k is {}'.format(k)
            try :
                kk = None
                kk = d[k]
                #print 'kk is {}'.format(kk)
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
            #D['val'] = d['val']
            pass


    def Print(self,d,l) :
        if 'success' in d.keys() :
            l.append(d['success'])
            l.append(d['failure'])
            print l
            del l[-1]
            del l[-1]
            return
        
        for k in d.keys() :
            l.append(k)
            self.Print(d[k],l)
            del l[-1]
        

N = NestedDict()
K = ['version','cipher']
N.SetKeys(K)

fname = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\mylog.txt'
with open(fname) as fp :
    for line in fp :
        print line
        d = json.loads(line)
        N.AddDict(d)

l = []
N.Print(N.keys,l)


