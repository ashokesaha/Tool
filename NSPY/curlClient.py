from botClient import *
import struct

class  curlClient (BotClient) :
    def __init__(self,ip,port) :
        super(self.__class__,self).__init__(ip,port)

    
    def ReadX(self,tout=0) :
        
        try :
            self.sd.settimeout(5)
            while 1:
                data = None
                data = self.sd.recv(tout)
                if  not data :
                    print 'No data Read'
                    break
                else :
                    print data

        except socket.timeout :
            print 'timeout happened. data {}'.format(data)
            pass
        return data


    


def Test() :
    cl = curlClient('10.102.28.71', 2346)
    cl.Connect()
    print 'connect done'
    bc = BotConfig()
    bc.setPeerlist(['10.102.28.232'])
    bc.setPortlist([8080,8081,8082])
    bc.setUrllist(['files/file_1','files/file_2'])
    bc.setCmdGET()
    #bc.setCert('client_one_cert.pem')
    #bc.setKey('client_one_key.pem')

    cl.SendCMD(bc)
    cl.Read(1024)

