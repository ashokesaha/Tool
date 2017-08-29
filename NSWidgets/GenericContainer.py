import  sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
from    PyQt5 import QtCore, QtGui, QtWidgets
import  CustomWidget
import  CertInstaller
from    BEOpenSSLServerDialog import *
from    BasicClientDialog     import *
from    DUTDialog import *

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
    TYPE_CONTAINER_NS = 105

    TYPE_NS_INSTALL_CERT = 201
    TYPE_NS_CLEAR_CONFIG = 202
    TYPE_NS_SELECT_DUT = 203


    CONTAINER_L1 = 1
    CONTAINER_L2 = 2
    CONTAINER_R2 = 3
    CONTAINER_R1 = 4
    CONTAINER_T1 = 5
    CONTAINER_NS = 6

    widgetTypeMap = [None, TYPE_CONTAINER_L1, CONTAINER_L2,
                        TYPE_CONTAINER_R2, TYPE_CONTAINER_R1,
                        TYPE_CONTAINER_T1,TYPE_CONTAINER_NS]
    

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
    typeMap[CONTAINER_NS] = [TYPE_NS_SELECT_DUT, TYPE_NS_INSTALL_CERT, TYPE_NS_CLEAR_CONFIG]



    colorMap = []
    colorMap.append(QtGui.QColor(0,0,0,250))
    colorMap.append(QtGui.QColor(50,50,50,250))
    colorMap.append(QtGui.QColor(50,50,50,250))
    colorMap.append(QtGui.QColor(50,50,50,250))
    colorMap.append(QtGui.QColor(50,50,50,250))
    colorMap.append(QtGui.QColor(50,50,50,250))
    colorMap.append(QtGui.QColor(50,50,50,250))
   



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
    nameMap[TYPE_NS_INSTALL_CERT]       = 'Install Cert'
    nameMap[TYPE_NS_CLEAR_CONFIG]       = 'Clear Config'
    nameMap[TYPE_NS_SELECT_DUT]         = 'Select DUT'


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
        
        self.contextMenuDialogMap[GenericContainer.TYPE_FE_OPENSSL_CLIENT] = BasicClientDialog(self)
        self.contextMenuDialogMap[GenericContainer.TYPE_FE_CURL_HTTPCLIENT] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_FE_CURL_SSL_CLIENT] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_FE_PIPELINE_SSL_CLIENT] = None
        
        self.contextMenuDialogMap[GenericContainer.TYPE_CRL_OPENSSL_SERVER ] = None
        self.contextMenuDialogMap[GenericContainer.TYPE_OCSP_OPENSSL_SERVER] = None

    

    def  __init__(self,containerType,parent=None) :
        super(self.__class__,self).__init__(None)
        self.container_type = containerType
        self.parent = parent
        self.entityList = []
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setSizeConstraint(0)
        self.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.496401, y1:0, x2:0.017, y2:0, stop:0.909605 rgba(150, 150, 150, 250), stop:1 rgba(20, 20, 20, 220));")
        self.backend_obj = None


    def paintEvent(self, event=None) :
        qP = QtGui.QPainter(self)
        qP.setRenderHint(QtGui.QPainter.Antialiasing)
        brush = QtGui.QBrush(GenericContainer.colorMap[self.container_type])
        qP.setBrush(brush)
        qP.drawRect(self.rect())


    def SetBackendObj(self,obj) :
        self.backend_obj = obj


    def GetBackendObj(self) :
        return self.backend_obj
    

    def GetType(self) :
        return GenericContainer.widgetTypeMap[self.container_type]


    def GetSess(self) :
        if (self.container_type == GenericContainer.CONTAINER_NS) :
            obj = self.GetBackendObj()
            return obj.GetSess()
        else :
            return self.parent.GetSess()

    

    def AddEntity(self,entityType) :
        W = CustomWidget.MyRectWidget(entityType)
        self.verticalLayout.addWidget(W)
        W.container = self
        self.entityList.append(W)
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

        w = None
        if act :
            t = act.data()
            dialog = QtWidgets.QDialog()

            if t == GenericContainer.TYPE_BE_OPENSSL_SERVER :
                w = BEOpenSSLServerDialog(self)

            elif t == GenericContainer.TYPE_FE_OPENSSL_CLIENT :
                w = BasicClientDialog(self)

            elif t == GenericContainer.TYPE_NS_SELECT_DUT :
                print 'TYPE_NS_SELECT'
                w = DUTDialog(self)

            elif t == GenericContainer.TYPE_NS_INSTALL_CERT :
                print 'TYPE_NS_INSTALL_CERT'
                obj = self.GetBackendObj()
                if not obj :
                    print 'No NS attached'
                    return
                if not obj.sess :
                    print 'No session with NS'
                    return
                ci = CertInstaller.CertInstall()
                ci.SetCertDir('C:\\Users\\ashokes\\Miniconda2\\NSPY\\Certs')
                #if obj.sess.isLogin() :
                #    obj.Logout()

                ci.PushToNS(obj.nsip)
                obj.Login()
                ci.Link(obj.sess)

            elif t == GenericContainer.TYPE_NS_CLEAR_CONFIG :
                print 'TYPE_NS_CLEAR_CONFIG'
                obj = self.GetBackendObj()
                if not obj :
                    print 'No NS attached'
                    return
##                if not obj.sess :
##                    print 'No session with NS'
##                    return
##                if not obj.sess.isLogin() :
##                    print 'Not logged in to NS'
##                    return
##                print 'clear config sess {} login {}'.format(obj.sess, obj.sess.isLogin())
                obj.Login()
                obj.sess.clear_config(level='basic')

            if w :
                w.setupUi(dialog)
                dialog.exec_()
        

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

    Form = GenericContainer(GenericContainer.CONTAINER_L1)
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    Form2 = GenericContainer(GenericContainer.CONTAINER_L2)
    ui2 = Ui_Form()
    ui2.setupUi(Form2)
    Form2.show()
    
    #Form.AddEntity(GenericContainer.TYPE_SSL_VSERVER)
    #Form.AddEntity(GenericContainer.TYPE_SSL_TCP_VSERVER)
    #Form.AddEntity(GenericContainer.TYPE_HTTP_VSERVER)
    #Form.AddEntity(GenericContainer.TYPE_TCP_VSERVER)
    #Form.show()
    sys.exit(app.exec_())
    

