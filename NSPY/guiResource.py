import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')

from   PyQt5.QtCore     import *
from   PyQt5.QtWidgets  import *
from   PyQt5.QtGui      import *

from   guiValidation    import *


##########################################################
class NSPYItemObj(QObject) :
    def __init__(self,row,name) :
        self.row = row
        self.name = name






###########################################################
class NSPYListWidget(QListWidget) :
    def __init__(self) :
        super(NSPYListWidget,self).__init__()
        self.itemList = []


    def addItem(self,name) :
        qobj = NSPYItemObj(self.count(),name)
        super(NSPYListWidget,self).addItem(name)
        self.itemList.append(qobj)
    

    def takeItem(self,row) :
        super(NSPYListWidget,self).takeItem(row)
        qobj = self.itemList[row]
        self.itemList.remove(qobj)


    def mouseDoubleClickEvent(self, e) :
        super(NSPYListWidget,self).mouseDoubleClickEvent(e)
        row = self.currentRow()
        if (row >= 0) :
            self.takeItem(row)




###############################################################
class NSPYResourceWidget(QWidget) :
    def __init__(self) :
        super(NSPYResourceWidget,self).__init__()
        self.NSPYBotList = []
        self.NSPYBEServerList = []

        self.pGreen = QPalette()
        self.pGreen.setColor(QPalette.Text,Qt.green)
        self.pRed = QPalette()
        self.pRed.setColor(QPalette.Text,Qt.red)
        self.pBlack = QPalette()
        self.pBlack.setColor(QPalette.Text,Qt.black)

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

        #self.nsip.setStyleSheet("background-color:gray; color:#00ffff;font-size:14pt;border-color:blue;border-style=solid;border-width:thick")
        self.nsip.setStyleSheet("font-size:14pt; border: 2px solid  red")

        self.lE = QLineEdit()
        self.lE.setToolTip("Enter a Bot IP")
        self.lE.returnPressed.connect(self.ListUpdate)
        vbox.addWidget(self.lE)
        
        self.qq = NSPYListWidget()
        self.qq.setToolTip("List of Active Bots")
        vbox.addWidget(self.qq)


        self.lE2 = QLineEdit()
        self.lE2.setToolTip("Enter a Server IP")
        self.lE2.returnPressed.connect(self.ServerUpdate)
        vbox.addWidget(self.lE2)
        
        self.qq2 = NSPYListWidget()
        self.qq2.setToolTip("List of Active Servers")
        vbox.addWidget(self.qq2)

        self.eRR = QLineEdit()
        self.eRR.setPalette(self.pRed)
        vbox.addWidget(self.eRR)



    def ListUpdate(self) :
        s = self.lE.text()
        self.lE.clear()
        cl = NSPYValidateCurlClient(s)
        if not cl :
            #self.nsipro.setPalette(self.pRed)
            s = NSPYGetErrStr()
            self.eRR.setText(NSPYGetErrStr())
        else :
            self.qq.addItem(s)
            self.NSPYBotList.append(cl)
            self.eRR.setPalette(self.pGreen)
            self.eRR.setText('Bot added ...')
    

    def NSIPUpdate(self) :
        s = self.nsip.text()
        self.nsip.clear()
        
        if not NSPYValidateNSIP(s) :
            self.eRR.setPalette(self.pRed)
            s = NSPYGetErrStr()
            self.eRR.setText(NSPYGetErrStr())
        else :
            self.eRR.setPalette(self.pGreen)
            self.nsipro.setPalette(self.pGreen)
            self.nsipro.setText(s)
            self.eRR.setText('NSIP connected')



    def ServerUpdate(self) :
        s = self.lE2.text()
        self.lE2.clear()
        beS = NSPYValidateBEServer(s)
        
        if not beS :
            self.eRR.setPalette(self.pRed)
            s = NSPYGetErrStr()
            self.eRR.setText(NSPYGetErrStr())
        else :
            self.qq2.addItem(s)
            self.NSPYBEServerList.append(beS)
            self.eRR.setPalette(self.pGreen)
            self.eRR.setText('BE Server added ...')
        



##############################################
if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = NSPYResourceWidget()
    ex.show()
    
    app.exec_()
