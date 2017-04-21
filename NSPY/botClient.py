import sys
import json
import socket
import time
import struct 




def BotTest(ip,port) :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((ip, port))
    s.sendall('Hello, world')
    time.sleep(2)
    data = s.recv(1024)
    s.close()
    print 'Received:: ', data





class  BotConfig() :
    def __init__(self) :
        self.ip = None
        self.port = None
        self.cert = None
        self.key = None
        self.version = None
        self.cipher = None
        self.reuse = None
        self.reneg = None
        self.timeout = None
        self.ckv = None
        self.prnt = None
        self.log = None
        self.iter = None
        self.err = None
        self.burst = None
        self.loop = None
        self.padtest = None
        self.smallrecordtest = None
        self.adminport = None
        self.inetd = None
        self.cmd = None

    def Clear(self) :
        self.ip = None
        self.port = None
        self.cert = None
        self.key = None
        self.version = None
        self.cipher = None
        self.reuse = None
        self.reneg = None
        self.timeout = None
        self.ckv = None
        self.prnt = None
        self.log = None
        self.iter = None
        self.err = None
        self.burst = None
        self.loop = None
        self.padtest = None
        self.smallrecordtest = None
        self.adminport = None
        self.inetd = None
        self.cmd = None


    def setIP(self,ip) :
        self.ip = ip

    def setPort(self,port) :
        self.port = port

    def setCert(self, cert) :
        self.cert = cert

    def setKey(self,key) :
        self.key = key

    def setVersion(self,version) :
        self.version = version

    def setCipher(self,cipher) :
        self.cipher = cipher

    def setReuse(self,reuse) :
        self.reuse = reuse

    def setReneg(self,reneg) :
        self.reneg = reneg

    def setTimeout(self,timeout) :
        self.timeout = timeout

    def setCkv(self,ckv) :
        self.ckv = ckv

    def setPrnt(self,prnt) :
        self.prnt = prnt

    def setLog(self,log) :
        self.log = log

    def setIter(self,iter) :
        self.iter = iter

    def setErr(self,err) :
        self.err = err

    def setBurst(self,burst) :
        self.burst = burst

    def setLoop(self,loop) :
        self.loop = loop

    def setPadtest(self,padtest) :
        self.padtest = padtest

    def setSmallrecordtest(self,smallrecordtest) :
        self.smallrecordtest = smallrecordtest

    def setAdminport(self,adminport) :
        self.adminport = adminport

    def setInetd(self,inetd) :
        self.inetd = inetd

    def setCmdGET(self) :
        self.cmd = "GET"

    def setCmdPUT(self) :
        self.cmd = "PUT"
    

    def ToJson(self) :
        dd = dict((k, v) for k, v in self.__dict__.iteritems()  if v)
        s = json.dumps(dd)
        return s

    


class  BotClient(object) :
    def __init__(self,ip,port) :
        self.ip = ip
        self.port = port
        self.sd = 0

    def Connect(self) :
        self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sd.connect ((self.ip, self.port))

    def SendCMD(self,cfg) :
        str = cfg.ToJson()
        lstr = struct.pack(">I", len(str))
        self.sd.sendall(lstr)
        self.sd.sendall(str)
        #self.sd.shutdown(socket.SHUT_WR)
        

    def Read(self,tout=0) :
        try :
            data = None
            len = 0
            data = self.sd.recv(4)
            if not data :
                return None
            
            len = struct.unpack("<I",data)
            
            while 1:
                data = self.sd.recv(len[0])
                if  not data :
                    break
                else :
                    print data

           
        except socket.timeout :
            pass
        return data  
       
    
   
        
def Test() :
    bt = BotClient('10.102.28.61', 2345)
    bt.Connect()
    
    bc = BotConfig()
    bc.setIP('10.102.28.15')
    bc.setPort(443)
    bc.setCert('client_one_cert.pem')
    bc.setKey('client_one_key.pem')

    bt.SendConfig(bc)
    bt.Read(0)
    



    
