import sys
import os
import time
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')


import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION

from nssrc.com.citrix.netscaler.nitro.resource.config.basic.service import service as NSSVC
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher import sslcipher as SSLCIPHER
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservice import sslservice as SSLSVC
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslciphersuite import sslciphersuite as SSLCIPHERSUITE
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher_sslciphersuite_binding  import  *


import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver
import nssrc.com.citrix.netscaler.nitro.service.nitro_service as NITROSVC
import nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip as NS
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as CERTKEY
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding import sslvserver_sslcertkey_binding as VsrvrCKeyBdg
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver  as LBVSERVER
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding  import *

from test_util    import *
from test_dut    import * 
from test_config import *
from TestException import *

import requests
import threading



#matplotlib.interactive(True)

import matplotlib.pyplot as plt

#plt.ion()

def Equ() :
    #ax^2 + bx + c
    C = [1.5,-4,-2]
    X = np.arange(0,3,0.1)
    Y = np.add(np.multiply(C[0],np.square(X)), C[1] * X) + C[2]
    plt.figure(1)
    plt.plot(X,Y,'b',linewidth=0.5)
    #plt.show()
    plt.figure(2)
    plt.plot(X,Y,'b',linewidth=0.5)
    plt.show()
    
    return

def Test1() :
    #plt.ion()
    fig = plt.figure()

    
    plt.plot([1,2,3,4])
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.plot([-1, 0, 1, 2], [1, 4, 9, 16])
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'rx')
    plt.axis([-2, 6, 0, 20])
    plt.ylabel('some numbers')
    plt.xlabel('x-axis')
    plt.show()

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    #sys.stdin.readline()




def onclick(event):
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))





def Test2() :
   
    
    plt.figure(1)                # the first figure
    plt.subplot(211)             # the first subplot in the first figure
    plt.plot([1, 2, 3])
    plt.pause(0.0001) 
    plt.subplot(212)             # the second subplot in the first figure
    plt.plot([4, 5, 6])
    plt.pause(5)

    plt.figure(2)                # a second figure
    plt.plot([4, 5, 6])          # creates a subplot(111) by default
    plt.pause(5)

    plt.figure(1)                # figure 1 current; subplot(212) still current
    plt.subplot(211)             # make subplot(211) in figure1 current
    plt.title('Easy as 1, 2, 3') # subplot 211 title
    plt.subplot(212)
    plt.title('subplot 212')
    plt.pause(5)

    plt.show()

    #sys.stdin.readline()
    #print 'out of readline'

    #plt.figure(1)
    #plt.subplot(211)
    #plt.pause(2)
    #plt.cla()
    #plt.show()

    #time.sleep(5)



def Test3() :
    os.chdir('C:\\Users\\ashokes\\Miniconda2\\NSPY')
    img=mpimg.imread('TestImage_1.png')
    
    plt.figure(1)                # the first figure
    
    plt.subplot(211)             # the first subplot in the first figure
    plt.plot([1, 2, 3])
    plt.pause(0.0001) 

    plt.subplot(212)             # the second subplot in the first figure
    imgplot = plt.imshow(img)
    plt.pause(0.1)

    plt.show()



def  Test4() :
    session = Login('10.102.28.201')
    CList = SSLCIPHERSUITE.get(session)
    DList = sslcipher_sslciphersuite_binding.get(session, "DH")
    
    
    l1 = [str(c.ciphername) for c in CList]
    l2 = [str(d.ciphername) for d in DList]

    s1 = set(l1)
    s2 = set(l2)
    s3 = s1 - s2

    print s1  
    print '\n'
    print s2
    print '\n'
    print s3
    print '\n'
    

#th1 = threading.Thread(target=Test1)
#th1.start()
#th1.join()

#Test1()

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()


def Test5() :
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('click to build line segments')
    #line, = ax.plot([0], [0])  # empty line
    #linebuilder = LineBuilder(line)

    plt.xticks([0,0.1,0.2,0.3,0.4,0.5])
    plt.show()
    print 'show called'





def SampleAPI() :
    # creating figures
    f1  = plt.figure()
    f10 = plt.figure(num=10)

    # closing figure
    plt.close('all')
    plt.close(10)

    




