import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *




########################################################################
class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        nameLabel = QLabel("Name:")
        self.nameLine = QLineEdit()
        self.submitButton = QPushButton("&Submit")

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(nameLabel)
        buttonLayout1.addWidget(self.nameLine)
        buttonLayout1.addWidget(self.submitButton)

        self.submitButton.clicked.connect(self.submitContact)

        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(buttonLayout1, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Hello Qt")

    def submitContact(self):
        name = self.nameLine.text()

        if name == "":
            QMessageBox.information(self, "Empty Field",
                                    "Please enter a name and address.")
            return
        else:
            QMessageBox.information(self, "Success!",
                                    "Hello %s!" % name)






########################################################################
class Example(QMainWindow):
    
    def __init__(self):
        super(Example,self).__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        hoverAction = QAction(QIcon('1.png'), 'Hover', self)
        exitAction.setStatusTip('Exit application')
        hoverAction.hovered.connect(self.hover)
        

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        hoverMenu = menubar.addMenu('&Hover')
        hoverMenu.addAction(hoverAction)
        

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar.addAction(hoverAction)
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')    
        self.show()


    def hover(self) :
        print 'hover action ..'
    
        





########################################################################
class Example2(QWidget):
    
    def __init__(self):
        super(Example2,self).__init__()
        self.initUI()
        
        
    def initUI(self):
        
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        #vbox = QVBoxLayout()
        #vbox.addStretch(1)
        #vbox.addWidget(okButton)
        #vbox.addWidget(cancelButton)
        #self.setLayout(vbox) 

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        #self.setLayout(hbox) 


        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()
        





########################################################################
class Example3(QWidget):
    
    def __init__(self):
        super(Example3,self).__init__()
        self.initUI()
        
        
    def initUI(self):
        
        grid = QGridLayout()
        self.setLayout(grid)
 
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                '4', '5', '6', '*',
                 '1', '2', '3', '-',
                '0', '.', '=', '+']
        
        positions = [(i,j) for i in range(5) for j in range(4)]
        
        for position, name in zip(positions, names):
            print 'position {} - {} {}'.format(position,*position)            
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)
            
        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()






########################################################################
class Example4(QWidget):
    
    def __init__(self):
        super(Example4,self).__init__()
        self.initUI()
        
        
    def initUI(self):
        
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)
        lcd.display(11)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')
        self.show()





########################################################################
class Example5(QWidget):
    
    def __init__(self):
        super(Example5,self).__init__()
        self.initUI()
        
        
    def initUI(self):      

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)
        
        self.le = QLineEdit(self)
        self.le.move(130, 22)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()
        
        
    def showDialog(self):
        
        text, ok = QInputDialog.getText(self, 'Input Dialog', 
            'Enter your name:')
        
        if ok:
            self.le.setText(str(text))





########################################################################
class Example6(QWidget):
    
    def __init__(self):
        super(Example6,self).__init__()
        self.initUI()
        
        
    def initUI(self):      

        col = QColor(0, 0, 0) 

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)

        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" 
            % col.name())
        self.frm.setGeometry(130, 22, 100, 100)            
        
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')
        self.show()
        
        
    def showDialog(self):
      
        col = QColorDialog.getColor()

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % col.name())





########################################################################
class Example7(QMainWindow):
    
    def __init__(self):
        super(Example7,self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 180)
        self.textEdit = QTextEdit(self)
        self.btn = QPushButton('Btn', self)
        x = self.textEdit.move(10,10)
        x = self.btn.move(30,30)
               
        #self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.show()
    


############################################################################
class Example8(QWidget):
    
    def __init__(self):
        super(Example8,self).__init__()
        self.initUI()
        
        
    def initUI(self):      

        cb = QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.changeTitle)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox')
        self.show()
        
        
    def changeTitle(self, state):
      
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle('')






#######################################################################
class Example9(QWidget):
    
    def __init__(self):
        super(Example9,self).__init__()
        self.initUI()
        
        
    def initUI(self):      

        self.col = QColor(0, 0, 0)       

        redb = QPushButton('Red', self)
        redb.setCheckable(True)
        redb.move(10, 10)

        redb.clicked[bool].connect(self.setColor)

        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)

        greenb.clicked[bool].connect(self.setColor)

        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)

        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %  
            self.col.name())

        self.textEdit = QTextEdit(self)
        self.textEdit.move(150,150)

        
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Toggle button')
        self.show()
        
        
    def setColor(self, pressed):

        source = self.sender()

        s = 'type(self) {}\n'.format(type(self))
        s += 'type(source) {}'.format(type(source))
        self.textEdit.setText(s)
        
        if pressed:
            val = 255
        else: val = 0
                        
        if source.text() == "Red":
            self.col.setRed(val)                
        elif source.text() == "Green":
            self.col.setGreen(val)             
        else:
            self.col.setBlue(val) 
            
        self.square.setStyleSheet("QFrame { background-color: %s }" %
            self.col.name())  






##########################################################################
class Button(QPushButton):
  
    def __init__(self, title, parent):
        super(Button,self).__init__(title,parent)
        print 'DragButton __init__'    

    def mouseMoveEvent(self, e):
        print 'DragButton  mouseMoveEvent'    
        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


    def mousePressEvent(self, e):
        print 'DragButton  mousePressEvent'    
        QPushButton.mousePressEvent(self, e)
        
        if e.button() == Qt.LeftButton:
            print('press')



#######################################################################
class Example10(QWidget):
  
    def __init__(self):
        super(Example10,self).__init__()
        self.initUI()
        
        
    def initUI(self):

        self.setAcceptDrops(True)

        self.button = Button('Button', self)
        self.button.move(20, 20)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 150)
        self.show()

    def dragEnterEvent(self, e):
        e.accept()
        

    def dropEvent(self, e):
        position = e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()






##########################################################

class QuickThread(QThread) :

    def __init__(self, w1) :
        super(QuickThread,self).__init__()
        self.w1 = w1
        
    def run(self) :
        self.w1.work()



class Worker(QObject) :
    sig = pyqtSignal(str)
    def __init__(self, num) :
        super(Worker,self).__init__()
        self.num = num

    @pyqtSlot(str)
    def work(self):
        while (self.num > 0) :
            s = '12345678901234567890' + str(QThread.currentThread()) + ':' + str(self.num)
            self.sig.emit(s)
            QThread.msleep(250)
            self.num = self.num - 1



class  ThreadTest(QMainWindow) :
    def __init__(self) :
        super(ThreadTest,self).__init__()
        self.initUI()

    def initUI(self):
        #self.tE = QTextEdit(self)
        #self.tE.setGeometry(300, 300, 280, 150)
        #self.show()

        self.setGeometry(300, 300, 250, 180)

        self.tE = QTextEdit(self)
        self.tE.setText('one')
        #self.setCentralWidget(self.tE)

        self.tEx = QTextEdit(self)
        self.tEx.setText('two')
        self.tEx.move(50,50)
        #self.setCentralWidget(self.tE)

        self.tEy = QTextEdit(self)
        self.tEy.setText('three')
        self.tEy.move(100,100)
        #self.setCentralWidget(self.tE)

        
        self.w1 = Worker(100)
        self.w1.sig[(str)].connect(self.dispText)
        self.qt1 = QuickThread(self.w1)
        self.qt1.start()
        

    @pyqtSlot(str)
    def  dispText(self,s) :
        #self.tE.append(str(self.w1.num))
        #self.tE.setText(str(self.w1.num))
        self.tE.append(s)







############################################################
class TabTest(QTabWidget) :
    def __init__(self) :
        super(TabTest,self).__init__()
        self.initUI()    

    def initUI(self):
        #self.qtw = QTabWidget(self)
        #self.qtw.setGeometry(300, 300, 280, 150)

        self.setGeometry(300, 300, 300, 300)
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        
        self.p1 = QWidget()
        self.p2 = QWidget()
        self.p3 = QWidget()
        
        self.te1 = QTextEdit(self.p1)
        self.te1.setText('one')
        self.te2 = QTextEdit(self.p2)
        self.te2.setText('two')
        self.te3 = QTextEdit(self.p3)
        self.te3.setText('three')
        
        self.addTab(self.p1, 'One')
        self.addTab(self.p2, 'Two')
        self.addTab(self.p3, 'Three')
        
        




############################################################
class TabTest2(QMainWindow) :
    def __init__(self) :
        super(TabTest2,self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 180)
        self.tbe = QTabWidget(self)
        self.setCentralWidget(self.tbe)

        self.te1 = QTextEdit()
        self.te1.setText('one')
        self.te2 = QTextEdit()
        self.te2.setText('two')
        self.te3 = QTextEdit()
        self.te3.setText('three')


        self.tbe.addTab(self.te1, 'Resource')
        self.tbe.addTab(self.te2, 'Two')
        self.tbe.addTab(self.te3, 'Three')
      
    





####################################################################

class QQListWidgetItem(QListWidgetItem) :
    def __init__(self) :
        super(QQListWidgetItem,self).__init__(type=1001)

    def mousePressEvent(self, e) :
        print 'QQ mousePressEvent ..'
        super(QQListWidgetItem,self).mousePressEvent(e)


    def mouseReleaseEvent(self, e) :
        print 'QQ mouseReleaseEvent ..'
        super(QQListWidgetItem,self).mouseReleaseEvent(e)

    def mouseMoveEvent(self, e) :
        print 'QQ mouseMoveEvent ..'
        super(QQListWidgetItem,self).mouseMoveEvent(e)




class ItemObj(QObject) :
    def __init__(self,row,name) :
        self.row = row
        self.name = name
    



class QQListWidget(QListWidget) :
    def __init__(self) :
        super(QQListWidget,self).__init__()
        self.itemList = []


    def addItem(self,name) :
        #print 'addItem: count {}'.format(self.count())
        qobj = ItemObj(self.count(),name)
        super(QQListWidget,self).addItem(name)
        #self.addItem(qobj.name)
        self.itemList.append(qobj)
    

    def takeItem(self,row) :
        super(QQListWidget,self).takeItem(row)
        qobj = self.itemList[row]
        self.itemList.remove(qobj)


    def mouseDoubleClickEvent(self, e) :
        super(QQListWidget,self).mouseDoubleClickEvent(e)
        row = self.currentRow()
        #print 'ListWidget mouseDoubleClickEvent ..{}'.format(self.currentRow())
        if (row >= 0) :
            self.takeItem(row)


    


##########################################################################
class ListTest(QMainWindow) :
    def __init__(self) :
        super(ListTest,self).__init__()
        self.initUI()

    def initUI(self):
        #self.setGeometry(300, 300, 250, 180)

        self.itm1 = QQListWidgetItem();
        self.itm2 = QQListWidgetItem();
        self.itm3 = QQListWidgetItem();
        self.itm4 = QQListWidgetItem();
        self.itm5 = QQListWidgetItem();
        self.itm6 = QQListWidgetItem();
        self.itm7 = QQListWidgetItem();
        self.itm8 = QQListWidgetItem();


        self.itm1.setText('one')
        self.itm2.setText('two')
        self.itm3.setText('three')
        self.itm4.setText('four')
        self.itm5.setText('five')
        self.itm6.setText('six')
        self.itm7.setText('seven')
        self.itm8.setText('eight')


        self.lw = QQListWidget(self)
        
        self.lw.addItem(self.itm1)
        self.lw.addItem(self.itm2)
        self.lw.addItem(self.itm3)
        self.lw.addItem(self.itm4)
        
        #self.setCentralWidget(self.lw)
        

    def mousePressEvent(self, e) :
        print 'ListTest mousePressEvent ..'
    
    def mouseReleaseEvent(self, e) :
        print 'ListTest mouseReleaseEvent ..'





class ListTest2(QWidget) :
    def __init__(self) :
        super(ListTest2,self).__init__()
        self.initUI()


    def initUI(self):

        vbox = QVBoxLayout()
        self.setLayout(vbox) 
        self.setGeometry(200,200,200,200)

        self.nsip = QLineEdit()
        self.nsip.setToolTip("Enter NSIP")
        self.nsip.returnPressed.connect(self.NSIPUpdate)
        vbox.addWidget(self.nsip)

        self.nsipro = QLineEdit()
        self.nsipro.setToolTip("Current NSIP")
        self.nsipro.setReadOnly(True)
        vbox.addWidget(self.nsipro)
        

        self.lE = QLineEdit()
        self.lE.setToolTip("Enter a Bot IP")
        self.lE.returnPressed.connect(self.ListUpdate)
        vbox.addWidget(self.lE)
        
        self.qq = QQListWidget()
        self.qq.setToolTip("List of Active Bots")
        vbox.addWidget(self.qq)


        self.lE2 = QLineEdit()
        self.lE2.setToolTip("Enter a Server IP")
        self.lE2.returnPressed.connect(self.ServerUpdate)
        vbox.addWidget(self.lE2)
        
        self.qq2 = QQListWidget()
        self.qq2.setToolTip("List of Active Servers")
        vbox.addWidget(self.qq2)



    def ListUpdate(self) :
        s = self.lE.text()
        self.lE.clear()
        self.qq.addItem(s)


    def NSIPUpdate(self) :
        pdef = self.nsip.palette()
        pGreen = QPalette()
        pGreen.setColor(QPalette.Text,Qt.green)
        pRed = QPalette()
        pRed.setColor(QPalette.Text,Qt.red)

        s = self.nsip.text()
        self.nsipro.setPalette(pGreen)
        self.nsipro.setText(s)


    def ServerUpdate(self) :
        s = self.lE2.text()
        self.lE2.clear()
        self.qq2.addItem(s)
        



###########################################################
class  MyWidget(QWidget) :
    def __init__(self):
        super(MyWidget,self).__init__()
        self.initUI()

    def initUI(self):
        print 'initUI..'
        self.setGeometry(300, 300, 250, 180)
        #QPushButton('Test',self)
        


    def  mousePressEvent(self,e) :
        if e.button() == Qt.LeftButton:
            print 'Left Button pressed'

        if e.button() == Qt.RightButton:
            print 'Right Button pressed'




##################################################################
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    ex = ListTest2()
    ex.show()
    
    #screen = Form()
    #screen.show()
    
    app.exec_()
    print 'app.exec exit'

