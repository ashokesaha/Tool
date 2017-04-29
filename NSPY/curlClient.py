from botClient import *
import struct

class  curlClient (BotClient) :
    def __init__(self,ip,port) :
        super(self.__class__,self).__init__(ip,port)

    


def Test() :
    cl = curlClient('10.102.28.61', 2346)
    cl.Connect()
    
    bc = BotConfig()
    bc.setIP('10.102.28.61')
    bc.setPort(8080)
    bc.setCmdGET()
    #bc.setCert('client_one_cert.pem')
    #bc.setKey('client_one_key.pem')

    cl.SendCMD(bc)
    cl.Read(0)
