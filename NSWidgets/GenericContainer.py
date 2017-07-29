import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
from PyQt5 import QtCore, QtGui, QtWidgets
import  CustomWidget
from BEOpenSSLServerDialog import *


class  GenericContainer (QtWidgets.QWidget)  :
    TYPE_SSL_VSERVER = 1
    TYPE_SSL_TCP_VSERVER = 2
    TYPE_HTTP_VSERVER = 3
    TYPE_TCP_VSERVER = 4

    TYPE_SSL_SERVICE = 5
    TYPE_SSL_TCP_SERVICE = 6
    TYPE_HTTP_SERVICE = 7
    TYPE_TCP_SERVICE = 8

    TYPE_BE_OPENSSL_SERVER = 9
    TYPE_BE_APACHE_SERVER = 10
    TYPE_BE_HTTP_DATA = 11

    TYPE_FE_OPENSSL_CLIENT = 12
    TYPE_FE_CURL_HTTPCLIENT = 13
    TYPE_FE_CURL_SSL_CLIENT = 14
    TYPE_FE_PIPELINE_SSL_CLIENT = 15

    TYPE_OCSP_OPENSSL_SERVER = 16
    TYPE_CRL_OPENSSL_SERVER = 17

    TYPE_CONTAINER_L1 = 101
    TYPE_CONTAINER_L2 = 102
    TYPE_CONTAINER_R2 = 103
    TYPE_CONTAINER_R1 = 104
    TYPE_CONTAINER_T1 = 105


    CONTAINER_L1 = 1
    CONTAINER_L2 = 2
    CONTAINER_R2 = 3
    CONTAINER_R1 = 4
    CONTAINER_T1 = 5

    widgetTypeMap = [None, TYPE_CONTAINER_L1, CONTAINER_L2,
                        TYPE_CONTAINER_R2, TYPE_CONTAINER_R1,
                        TYPE_CONTAINER_T1]
    

    typeMap = dict()
    typeMap[CONTAINER_L1] = [TYPE_FE_OPENSSL_CLIENT, TYPE_FE_CURL_HTTPCLIENT,
                             TYPE_FE_CURL_SSL_CLIENT,TYPE_FE_PIPELINE_SSL_CLIENT]
    typeMap[CONTAINER_L2] = [TYPE_SSL_VSERVER,TYPE_SSL_TCP_VSERVER,
                             TYPE_HTTP_VSERVER,TYPE_TCP_VSERVER]
    typeMap[CONTAINER_R2] = [TYPE_SSL_SERVICE, TYPE_SSL_TCP_SERVICE,
                             TYPE_HTTP_SERVICE,TYPE_TCP_SERVICE]
    typeMap[CONTAINER_R1] = [TYPE_BE_OPENSSL_SERVER, TYPE_BE_APACHE_SERVER,
                             TYPE_BE_HTTP_DATA]
    typeMap[CONTAINER_T1] = [TYPE_OCSP_OPENSSL_SERVER, TYPE_CRL_OPENSSL_SERVER]


    nameMap = dict()
    nameMap[TYPE_SSL_VSERVER]           = 'SSL Vserver'
    nameMap[TYPE_SSL_TCP_VSERVER]       = 'SSL_TCP Vserver'
    nameMap[TYPE_HTTP_VSERVER]          = 'HTTP Vserver'
    nameMap[TYPE_TCP_VSERVER ]          = 'TCP Vserver'
    nameMap[TYPE_SSL_SERVICE]           = 'SSL Service'
    nameMap[TYPE_SSL_TCP_SERVICE]       = 'SSL_TCP Service'
    nameMap[TYPE_HTTP_SERVICE]          = 'HTTP Service'
    nameMap[TYPE_TCP_SERVICE]           = 'TCP Service'
    nameMap[TYPE_BE_OPENSSL_SERVER]     = 'OpenSSL Server'
    nameMap[TYPE_BE_APACHE_SERVER]      = 'Apache Server'
    nameMap[TYPE_BE_HTTP_DATA]          = 'Http Data Server'
    nameMap[TYPE_FE_OPENSSL_CLIENT]     = 'OpenSSL Client'
    nameMap[TYPE_FE_CURL_HTTPCLIENT]    = 'Curl HTTP Client'
    nameMap[TYPE_FE_CURL_SSL_CLIENT]    = 'Curl SSL Client'
    nameMap[TYPE_FE_PIPELINE_SSL_CLIENT]= 'Pipeline Client'
    nameMap[TYPE_CRL_OPENSSL_SERVER]    = 'CRL Server'
    nameMap[TYPE_OCSP_OPENSSL_SERVER]   = 'OCSP Server'


    def SetupContextMenuDialogMap(self) :
        self.contextMenuDialogMap[GenericContainer.TYPE_SSL_VSERVER] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_SSL_TCP_VSERVER] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_HTTP_VSERVER] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_TCP_VSERVER] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_SSL_SERVICE] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_SSL_TCP_SERVICE] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_HTTP_SERVICE] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_TCP_SERVICE] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_BE_OPENSSL_SERVER] = BEOpenSSLServerDialog(self)
        self.contextMenuDialogMap[GenericContainer.TYPE_BE_APACHE_SERVER] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_BE_HTTP_DATA] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_FE_OPENSSL_CLIENT] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_FE_CURL_HTTPCLIENT] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_FE_CURL_SSL_CLIENT] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_FE_PIPELINE_SSL_CLIENT] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_CRL_OPENSSL_SERVER ] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_OCSP_OPENSSL_SERVER] = None

    

    def  __init__(self,containerType,parent=None) :
        super(self.__class__,self).__init__(parent)
        self.container_type = containerType
        self.entityList = []
        self.contextMenuDialogMap = dict()
        self.SetupContextMenuDialogMap()
        self.setFixedWidth(80)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setSizeConstraint(0)
        #self.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(120, 120, 120, 250), stop:1 rgba(20, 20, 20, 220));")
        self.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(150, 150, 150, 250), stop:1 rgba(20, 20, 20, 220));")


    def GetType(self) :
        return GenericContainer.widgetTypeMap[self.container_type]
    

    def AddEntity(self,entityType) :
        W = CustomWidget.MyRectWidget(entityType)
        self.verticalLayout.addWidget(W)
        W.container = self
        self.entityList.append(W)
        #print 'entity widget created {}'.format(W)
        return W


    def contextMenuEvent(self, event) :
        menu = QtWidgets.QMenu(self)
        actionList = []
        typeS = GenericContainer.typeMap[self.container_type]
        for t in typeS :
            name = GenericContainer.nameMap[t]
            act = menu.addAction(name)
            qv = QtCore.QVariant(t)
            act.setData(qv)
            actionList.append(act)

        act = menu.exec_(event.globalPos())
        t = act.data()
        dialog = QtWidgets.QDialog()
        self.contextMenuDialogMap[t].setupUi(dialog)
        dialog.exec_()
        #for w in self.entityList :
        #    print 'widget {} backend {}'.format(w,w.backend_obj)


    def  RegisterContextMenuDialog(self,type,W) :
        GenericContainer.contextMenuDialogMap[type] = W
    




class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(70, 100)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))



   
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = GenericContainer(GenericContainer.CONTAINER_R1)
    ui = Ui_Form()
    ui.setupUi(Form)
    #Form.AddEntity(GenericContainer.TYPE_SSL_VSERVER)
    #Form.AddEntity(GenericContainer.TYPE_SSL_TCP_VSERVER)
    #Form.AddEntity(GenericContainer.TYPE_HTTP_VSERVER)
    #Form.AddEntity(GenericContainer.TYPE_TCP_VSERVER)
    Form.show()
    sys.exit(app.exec_())
    

