import sys
import json
import socket
import time
import struct
import io

import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION



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
        self.cauth = None
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
        self.urllist = None
        self.peerlist = None
        self.portlist = None
        self.peeripport = None
        self.testid = None
        self.respsize = None
        self.recordsize = None
        self.delay = None

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
        self.urllist = None
        self.peerlist = None
        self.portlist = None
        self.peeripport = None
        seld.testid = None


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

    def setPeerlist(self, peers) :
        self.peerlist = peers

    def setPortlist(self, ports) :
        self.portlist = ports

    def setPeeripport(self, ipport) :
        self.peeripport = ipport
    
    
    def setUrllist(self, urls) :
        self.urllist = urls

    def setTestId(self, testid) :
        self.testid = testid
    

    def ToJson(self) :
        dd = dict((k, v) for k, v in self.__dict__.iteritems()  if v)
        s = json.dumps(dd)
        return s

    


class  BotClient(object) :
    id = 1
    
    def __init__(self,ip,port) :
        self.ip = ip
        self.port = port
        self.sd = 0
        self.bc = None
        self.logname = 'test.log'
        self.textio = None
        self.harness = None
        self.id = self.__class__.id
        self.matchtoken = None
        self.__class__.id = self.__class__.id + 1

    def  SetMatchToken(self,token) :
        self.matchtoken = token


    def Connect(self, timeout=5.0) :
        ret = True
        try :
            self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sd.settimeout(timeout)
            self.sd.connect ((self.ip, self.port))

            str = 'twinkletwinkle'
            lstr = struct.pack(">I", len(str))
            self.sd.sendall(lstr)
            self.sd.sendall(str)

            data = self.ReadOnce()
            if not data :
                ret = False
                return ret
            #if not data.__eq__('littlestar'):
            print 'data read {}'.format(data)
            if not data.__eq__(self.matchtoken):
                ret = False
                return ret
            
        except socket.error as e :
            ret = False

        print 'connect returning {}'.format(ret)
        return ret




    def SetHarness(self, harness) :
        self.harness = harness



    def SendCMD(self) :
        #self.OpenLog(self.ip)
        str = self.bc.ToJson()
        print 'sendCmd::{}'.format(str)
        lstr = struct.pack(">I", len(str))
        self.sd.sendall(lstr)
        self.sd.sendall(str)
        #self.sd.shutdown(socket.SHUT_WR)


    def SendClose(self) :
        str = ''
        lstr = struct.pack(">I", len(str))
        self.sd.sendall(lstr)
        
        
    def OpenLog(self,name=None) :
        if self.textio :
            self.CloseLog()
        
        if name :
            self.logname = name
        
        self.textio = io.open(self.logname, mode='at', buffering=1024)

    

    def Log(self,b) :
        self.textio.write(b)

    

    def CloseLog(self) :
        print 'closing Log.....'
        if not self.textio :
            return

        raise NITROEXCEPTION()
        self.textio.flush()
        self.textio.close()
        self.textio = None
    

    def SetConfig(self, bc) :
        self.bc = bc
    
        

    def  ReadOnce(self) :
        data = self.sd.recv(4)
        if not data :
            return data

        len = struct.unpack("<I",data)
        if(len[0] == 0) :
            return None

        data = self.sd.recv(len[0])
        return data




    # This read would be called when we expect all the
    # results from the client to come back. Only Client is now
    # writing the results of its tests. We should just keep on reading
    # till client is done.
    # If we one to read one transaction, call ReadOnce
    
    def Read(self,tout=0) :
        try :
           
            while(1) :
                data = None
                
                data = self.sd.recv(4)
                if not data :
                    break
                
                len = struct.unpack("<I",data)
                if(len[0] == 0) :
                    #self.CloseLog()
                    break
                data = self.sd.recv(len[0])
                #self.Log(u"{}".format(data))
                self.harness.Log('{}'.format('  ' + data))

        except socket.timeout as e:
            pass
        return data



    def  Dump(self) :
        s = 'BOT:: {} {} {}'.format(self.id,self.ip,self.port)
        self.harness.Log(s)
       
    
   
        
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
    



    
