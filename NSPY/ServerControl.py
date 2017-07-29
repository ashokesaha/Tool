import sys
from botClient import *
import struct

class  ServerControl (BotClient) :
    def __init__(self,ip,port) :
        super(self.__class__,self).__init__(ip,port)
        self.SetMatchToken('howiwonder')

    

    
def Test() :
    cl = ServerControl('10.102.28.61',2347)
    if not cl.Connect() :
        print 'connect failed'
        return
    bc = BotConfig()
    bc.setIP('10.102.28.61')
    bc.setPort(4545)
    cl.SetConfig(bc)
    cl.SendCMD()

    cl2 = ServerControl('10.102.28.61',2347)
    if not cl2.Connect() :
        print 'connect failed'
        return
    bc2 = BotConfig()
    bc2.setIP('10.102.28.61')
    bc2.setPort(4747)
    cl2.SetConfig(bc2)
    cl2.SendCMD()
    
    print 'Waiting'
    while(True) :
        pass
    

