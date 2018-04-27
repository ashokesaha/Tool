import sys
import os
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
import numpy as np
import scipy as sp


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.markers import MarkerStyle


progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass




class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        self.axes.plot(t, s)




class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [np.random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()




class MyScatterPlot(MyMplCanvas):

    def compute_initial_figure(self):
        X = [np.random.rand() for i in np.arange(1,20)]
        X = np.array(X)

        Y = [np.random.rand() for i in np.arange(1,20)]
        Y = np.array(Y)

        self.axes.scatter(X,Y, c = 10 * np.abs(X-Y), marker='^')

        X = [np.random.rand() for i in np.arange(1,20)]
        X = np.array(X)
        self.axes.scatter(X,Y, c = 10 * np.abs(X-Y), marker='*')
     





class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                    """embedding_in_qt5.py example
Copyright 2005 Florent Rougon, 2006 Darren Dale, 2015 Jens H Nielsen

This program is a simple example of a Qt5 application embedding matplotlib
canvases.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation.

This is modified from the embedding in qt4 example to show the difference
between qt4 and qt5"""
                                )

##
##qApp = QtWidgets.QApplication(sys.argv)
##
##aw = ApplicationWindow()
##aw.setWindowTitle("%s" % progname)
##aw.show()
##sys.exit(qApp.exec_())



class TestContainer(QtWidgets.QWidget):

    def  __init__(self, parent=None):
        super(self.__class__,self).__init__(parent)
        self.layout = None

    def setupUi(self):
        self.resize(400, 400)
        self.layout = QtWidgets.QVBoxLayout(self)

        dc = MyScatterPlot(None,width=5, height=4, dpi=100)
        self.layout.addWidget(dc)




class  DateSetTest(QtWidgets.QWidget):
    def  __init__(self, parent=None):
        super(self.__class__,self).__init__(parent)
        self.layout = None

    def setupUi(self) :
        D=sp.genfromtxt(r'C:\Users\ashokes\datingTestSet.txt',usecols=(0,1,2))
        Dmax = np.max(D,axis=0)
        Dmin = np.min(D,axis=0)
        Dnorm = (D - Dmin)/(Dmax - Dmin)
        Dnorm = Dnorm[0:100,:]

        M = dict()
        M['didntLike']  = 1
        M['smallDoses'] = 2
        M['largeDoses'] = 3
        
        Y=sp.genfromtxt(r'C:\Users\ashokes\datingTestSet.txt',usecols=3, dtype='S10')
        Y = [M[y] for y in Y]
        Y = Y[0:100]

        print Dnorm
        print Y
        I = Y==1
        print I
        #print Dnorm[Y==1]

        l = QtWidgets.QVBoxLayout(self)
        
        fig = Figure(figsize=(10, 10), dpi=100)
        figCanvas = FigureCanvas(fig)
        l.addWidget(figCanvas)
        self.axes1 = fig.add_subplot(111)
        hs=self.axes1.scatter(Dnorm[:,0], Dnorm[:,1], c=Y, label=('one','two','three'))
        self.axes1.set_xlabel('Freq Flyer')
        self.axes1.set_ylabel('Video Games')
        self.axes1.legend()




def f(t):
    return np.exp(-t) * np.cos(5*2*np.pi*t)


def f10(t):
    return 10.0 * np.exp(-t) * np.cos(2*np.pi*t)




class  ZoomTest(QtWidgets.QWidget):
    def  __init__(self, parent=None):
        super(self.__class__,self).__init__(parent)
        self.layout = None
        self.margin = 0.0
        self.ax1 = None
        self.figcanvas = None
        self.t1 = None
        self.layout = None


    def setupUi(self) :
        rcp = matplotlib.rcParams
##        for k in rcp.keys() :
##            print '{} --  {}'.format(k,rcp[k])
        
        matplotlib.rcParams['figure.facecolor'] = '#44aa88'
        matplotlib.rcParams['axes.edgecolor'] = '#0000aa'
        
        self.layout = QtWidgets.QVBoxLayout(self)
        fig = Figure(figsize=(6, 6), dpi=100, tight_layout=True)
        self.figcanvas = FigureCanvas(fig)
        self.layout.addWidget(self.figcanvas)

        self.t1 = np.arange(0.0, 3.0, 0.01)

        self.ax1 = fig.add_subplot(111)
        self.ax1.margins(self.margin)           # Default margin is 0.05, value 0 means fit
        self.ax1.plot(self.t1, f(self.t1), 'k')
        self.ax1.plot(self.t1, f10(self.t1), 'k')
        self.ax1.tick_params(axis='x',direction='in', labelcolor='#0000aa', labelsize=8.1)
        self.ax1.axhspan(0,4, xmin=0.01,xmax=0.99, fill=False)


##        ax2 = fig.add_subplot(221)
##        ax2.margins(0.2, 0.2)           # Values >0.0 zoom out
##        ax2.plot(t1, f(t1), 'r')
##        ax2.set_title('Zoomed out')
##
##        ax3 = fig.add_subplot(222)
##        ax3.margins(x=0, y=0.25)   # Values in (-0.5, 0.0) zooms in to center
##        ax3.plot(t1, f(t1), 'g')
##        ax3.set_title('Zoomed in')


    def Redraw(self) :
        self.ax1.cla()
        self.ax1.set_ylim(bottom=self.bottom,top=self.top) 
        #self.ax1.margins(y=self.margin)
        self.ax1.plot(self.t1, f(self.t1), 'k')
        self.ax1.plot(self.t1, f10(self.t1), 'k')
        self.figcanvas.draw()



    def mousePressEvent(self,e) :
        print 'mousePressEvent .. margin {}'.format(self.margin)
        tup = self.ax1.get_ylim()
        print 'y_lim ({},{})'.format(tup[0],tup[1])

        bottom = tup[0]
        top = tup[1]
        w = top - bottom
        w = 0.1 * w


        if e.button() == QtCore.Qt.LeftButton :
            top += w/2
            bottom -= w/2
##            
##            self.margin += 0.1
##            if (self.margin > 1.0) :
##                self.margin = 1.0
        elif e.button() == QtCore.Qt.RightButton :
            top -= w/2
            bottom += w/2

##            self.margin -= 0.1
##            if (self.margin < 0.0) :
##                self.margin = 0.0

        self.bottom = bottom
        self.top = top
        
        #self.ax1.set_ylim(bottom=bottom,top=top) 
        self.Redraw()



    def mouseDoubleClickEvent(self,e) :
        print 'mouseDoubleClickEvent..'
        




class  BarTest (QtWidgets.QWidget):
    def  __init__(self, parent=None):
        super(self.__class__,self).__init__(parent)
        self.layout = None
        self.axes = None

    def setupUi(self) :
        l = QtWidgets.QHBoxLayout(self)
        
        fig = Figure(figsize=(1, 3), dpi=100)
        figCanvas = FigureCanvas(fig)
        fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=None, hspace=None)

        l.addWidget(figCanvas)
        self.axes1 = fig.add_subplot(131)
        self.axes2 = fig.add_subplot(132)
        self.axes3 = fig.add_subplot(133)
        
        #self.axes1 = fig.add_subplot(131, frameon=False)
        self.axes1.get_xaxis().set_visible(False)
        self.axes1.get_yaxis().set_visible(False)
        self.axes1.autoscale(tight=True)
        #self.axes1.set_position([0,0,1,1])

        #self.axes2 = fig.add_subplot(132, frameon=False)
        self.axes2.get_xaxis().set_visible(False)
        self.axes2.get_yaxis().set_visible(False)
        self.axes2.autoscale(tight=True)
        #self.axes2.set_position([0,0,1,1])


        #self.axes3 = fig.add_subplot(133, frameon=False)
        self.axes3.get_xaxis().set_visible(False)
        self.axes3.get_yaxis().set_visible(False)
        self.axes3.autoscale(tight=True)
        #self.axes3.set_position([0,0,1,1])



        v1 = [100]
        v2 = [50]
        left = [0]
        lbl = ['mem']
        width = 0.35


        self.axes1.set_yticks([0,100,200])
        self.axes1.axis('on')
        self.axes1.set_ylim(0,200)
        self.axes1.grid(b=True,color='r', linestyle='-', linewidth=2)
        #self.axes1.set_yticks([v1[0],v1[0]+v2[0]])

        p1 = self.axes1.bar(left,v1,width)
        p2 = self.axes1.bar(left,v2,width,bottom=v1, tick_label=lbl)
        self.axes1.set_facecolor('k')

        self.axes1.text(0.0,v1[0]/2,'ash',
                        rotation='vertical',horizontalalignment='center',
                        verticalalignment='center')

        self.axes1.text(0.0,v1[0] + v2[0]/2,'ash',
                        rotation='vertical',horizontalalignment='center',
                        verticalalignment='center')



        self.axes2.set_yticks([0,100,200])
        self.axes2.axis('on')
        self.axes2.set_ylim(0,200)
        self.axes2.grid(b=True,color='r', linestyle='-', linewidth=2)

        p1 = self.axes2.bar(left,v1,width)
        p2 = self.axes2.bar(left,v2,width,bottom=v1, tick_label=lbl)
        self.axes2.set_facecolor('k')

        self.axes2.text(0.0,v1[0]/2,'ash',
                        rotation='vertical',horizontalalignment='center',
                        verticalalignment='center')

        self.axes2.text(0.0,v1[0] + v2[0]/2,'ash',
                        rotation='vertical',horizontalalignment='center',
                        verticalalignment='center')


        self.axes3.set_yticks([0,100,200])
        self.axes3.axis('on')
        self.axes3.set_ylim(0,200)
        self.axes3.grid(b=True,color='r', linestyle='-', linewidth=2)

        p1 = self.axes3.bar(left,v1,width)
        p2 = self.axes3.bar(left,v2,width,bottom=v1, tick_label=lbl)
        self.axes3.set_facecolor('k')

        self.axes3.text(0.0,v1[0]/2,'ash',
                        rotation='vertical',horizontalalignment='center',
                        verticalalignment='center')

        self.axes3.text(0.0,v1[0] + v2[0]/2,'ash',
                        rotation='vertical',horizontalalignment='center',
                        verticalalignment='center')







if __name__ == "__main__":
##    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = TestContainer()
    Form = DateSetTest()
    Form = BarTest()
    Form = ZoomTest()
    Form.setupUi()
    Form.show()
    sys.exit(app.exec_())


