import sys
import os
import time
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

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
    plt.plot([1,2,3,4])
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.plot([-1, 0, 1, 2], [1, 4, 9, 16])
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'rx')
    plt.axis([-2, 6, 0, 20])
    plt.ylabel('some numbers')
    plt.xlabel('x-axis')
    plt.show()

    sys.stdin.readline()



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


Test3()

class C(object) :
    def __init__(self,name,id) :
        self.name = name
        self.id = id

    def __cmp__(self,other) :
        print '__cmp__ test :'
        if((self.name == other.name) and (self.id == other.id)) :
            print 'returning true'
            return True
        return False

    def __eq__(self,other) :
        print '__eq__ test :'
        if((self.name == other.name) and (self.id == other.id)) :
            print 'returning true'
            return True
        return False
    

