import  sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSWidgets')

from    PyQt5 import QtCore, QtGui, QtWidgets
import  CustomWidget
import  CertInstaller

from    BasicClientDialog     import *
from    DUTDialog             import *
from    ocsp_responder        import *
from    SSLVServerDialog      import *
import  BEOpenSSLServerDialog



class  GenericContainer (QtWidgets.QWidget)  :
    botProbe = QtCore.pyqtSignal(str)
    
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

    TYPE_SAVE = 18
    TYPE_LOAD = 19
    TYPE_TEST_TMPLT_ONE = 20
    

    TYPE_CONTAINER_L1 = 101
    TYPE_CONTAINER_L2 = 102
    TYPE_CONTAINER_R2 = 103
    TYPE_CONTAINER_R1 = 104
    TYPE_CONTAINER_T1 = 105
    TYPE_CONTAINER_NS = 105
    TYPE_CONTAINER_NSHOLDER = 106
    TYPE_CONTAINER_BOT = 107

    TYPE_NS_INSTALL_CERT = 201
    TYPE_NS_CLEAR_CONFIG = 202
    TYPE_NS_SELECT_DUT = 203
    TYPE_NS_SELECT_NONE = 204
    TYPE_NS_REFRESH_BOT = 205
    

    CONTAINER_L1 = 1
    CONTAINER_L2 = 2
    CONTAINER_R2 = 3
    CONTAINER_R1 = 4
    CONTAINER_T1 = 5
    CONTAINER_NS = 6
    CONTAINER_NSHOLDER = 7
    CONTAINER_BOT = 8

    widgetTypeMap = [None, TYPE_CONTAINER_L1, CONTAINER_L2,
                        TYPE_CONTAINER_R2, TYPE_CONTAINER_R1,
                        TYPE_CONTAINER_T1,TYPE_CONTAINER_NS,
                     TYPE_CONTAINER_NSHOLDER,TYPE_CONTAINER_BOT]
    

    typeMap = dict()
    typeMap[CONTAINER_L1] = [TYPE_FE_OPENSSL_CLIENT, TYPE_FE_CURL_HTTPCLIENT,
                             TYPE_FE_CURL_SSL_CLIENT,TYPE_FE_PIPELINE_SSL_CLIENT,
                             TYPE_SAVE, TYPE_LOAD]
    typeMap[CONTAINER_L2] = [TYPE_SSL_VSERVER,TYPE_SSL_TCP_VSERVER,
                             TYPE_HTTP_VSERVER,TYPE_TCP_VSERVER,
                             TYPE_SAVE, TYPE_LOAD]
    typeMap[CONTAINER_R2] = [TYPE_SSL_SERVICE, TYPE_SSL_TCP_SERVICE,
                             TYPE_HTTP_SERVICE,TYPE_TCP_SERVICE,
                             TYPE_SAVE, TYPE_LOAD]
    typeMap[CONTAINER_R1] = [TYPE_BE_OPENSSL_SERVER, TYPE_BE_APACHE_SERVER,
                             TYPE_BE_HTTP_DATA,TYPE_SAVE, TYPE_LOAD]
    typeMap[CONTAINER_T1] = [TYPE_OCSP_OPENSSL_SERVER, TYPE_CRL_OPENSSL_SERVER,
                             TYPE_SAVE, TYPE_LOAD]
    typeMap[CONTAINER_NS] = [TYPE_NS_SELECT_DUT, TYPE_NS_INSTALL_CERT,
                             TYPE_NS_CLEAR_CONFIG, TYPE_TEST_TMPLT_ONE]

    typeMap[CONTAINER_NSHOLDER] = []
    typeMap[CONTAINER_BOT] = [TYPE_NS_REFRESH_BOT]


    saveFileName = dict()
    saveFileName[CONTAINER_L1] = 'L1.save'
    saveFileName[CONTAINER_L2] = 'L2.save'
    saveFileName[CONTAINER_R1] = 'R1.save'
    saveFileName[CONTAINER_R2] = 'R2.save'
    saveFileName[CONTAINER_T1] = 'T1.save'
    saveFileName[CONTAINER_NS] = 'NS.save'




    colorMap = []
    colorMap.append(QtGui.QColor(0,100,100,150))
    colorMap.append(QtGui.QColor(0,100,100,150))
    colorMap.append(QtGui.QColor(0,100,100,150))
    colorMap.append(QtGui.QColor(0,100,100,150))
    colorMap.append(QtGui.QColor(0,100,100,150))
    colorMap.append(QtGui.QColor(0,100,100,150))
    colorMap.append(QtGui.QColor(0,100,100,250))
    colorMap.append(QtGui.QColor(0,100,100,150))
    colorMap.append(QtGui.QColor(0,100,100,150))
    colorMap.append(QtGui.QColor(0,50,100,150))
   



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
    nameMap[TYPE_SAVE]                  = 'Save'
    nameMap[TYPE_LOAD]                  = 'Load'
    nameMap[TYPE_TEST_TMPLT_ONE]        = 'TestTemplateOne'
    nameMap[TYPE_NS_REFRESH_BOT]        = 'Refresh Botlist'


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

        if  self.container_type == GenericContainer.CONTAINER_T1 :
            self.myLayout = QtWidgets.QHBoxLayout(self)
        else :
            self.myLayout = QtWidgets.QVBoxLayout(self)
            
        self.myLayout.setSizeConstraint(0)

        if self.container_type == GenericContainer.CONTAINER_BOT :
            self.myLayout.setSpacing(2)
            QM = QtCore.QMargins(1,1,1,1)
            self.myLayout.setContentsMargins(QM)
        else :
            self.myLayout.setSpacing(8)
            
        self.myLayout.setAlignment(QtCore.Qt.AlignCenter)
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


    def GetCurDUT(self) :
        return self.parent.GetCurDUT()


    def SetCurDUT(self,dut) :
        self.parent.SetCurDUT(dut)        

    def AddDUT(self,dut) :
        self.parent.AddDUT(dut)


    def AddToSSLBEServerList(self,e) :
        self.parent.AddToSSLBEServerList(e)


    def AddEntity(self,entityType) :
        W = CustomWidget.MyRectWidget(entityType)
        self.myLayout.addWidget(W)
        W.container = self
        self.entityList.append(W)
        return W


    def contextMenuEvent(self, event) :
        if not self.GetCurDUT() :
            return
        
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
                w = BEOpenSSLServerDialog.BEOpenSSLServerDialog(self)

            elif t == GenericContainer.TYPE_FE_OPENSSL_CLIENT :
                w = BasicClientDialog(self)

            elif t == GenericContainer.TYPE_OCSP_OPENSSL_SERVER :
                w = OcspResponderDialog(self)

            elif t == GenericContainer.TYPE_NS_SELECT_DUT :
                w = DUTDialog(self)

            elif t == GenericContainer.TYPE_SSL_VSERVER :
                w = SSLVServerDialog(self)

            elif t == GenericContainer.TYPE_NS_INSTALL_CERT :
                obj = self.GetBackendObj()
                if not obj :
                    print 'No NS attached'
                    return
                if not obj.sess :
                    print 'No session with NS'
                    return
                ci = CertInstaller.CertInstall()
                ci.SetCertDir('C:\\Users\\ashokes\\Miniconda2\\NSPY\\Certs')

                ci.PushToNS(obj.nsip)
                obj.Login()
                ci.Link(obj.sess)

            elif t == GenericContainer.TYPE_NS_CLEAR_CONFIG :
                obj = self.GetBackendObj()
                if not obj :
                    return
                obj.Login()
                obj.sess.clear_config(level='basic')


            elif t == GenericContainer.TYPE_SAVE :
                fname = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\' + GenericContainer.saveFileName[self.container_type]
                saveFp = open(fname,'w')
                for e in self.entityList :
                    o = e.GetBackendObj()
                    s = o.ToFileStr() + '\n'
                    saveFp.write(s)
                saveFp.close()


            elif t == GenericContainer.TYPE_LOAD :
                fname = 'C:\\Users\\ashokes\\Miniconda2\\PyLogs\\' + GenericContainer.saveFileName[self.container_type]
                dut = self.GetCurDUT()
                if dut :
                    sess = dut.sess
                else :
                    sess = None
                
                try :
                    with open(fname) as f:
                        for line in f :
                            o = GenericContainer.FromFileStr(line,sess)
                            w = self.AddEntity(o.GetType())
                            w.SetBackendObj(o)
                            o.sigStatus.connect(w.slotStatus)

                            if (o.GetType() == GenericContainer.TYPE_BE_OPENSSL_SERVER) :
                                self.parent.AddToSSLBEServerList(o)
                                #o.Connect()
                                #o.SendOnce()
                                o.Start()
                                d = self.GetCurDUT()
                                if d :
                                    lR = d.logReader
                                    if lR :
                                        lR.RegisterObj(o)

                            
                    w = None
                except IOError as e :
                    print 'IOError happened'


            elif t == GenericContainer.TYPE_TEST_TMPLT_ONE:
                tt = TestTemplateOne('tone', self.GetSess())
                tt.Apply()

            elif t == GenericContainer.TYPE_NS_REFRESH_BOT:
                if self.isProbing :
                    print 'isProbing set.. not probing'
                    return
                self.isProbing = True
                self.b = BotProber('10.102.28')
                self.b.probeSig.connect(self.BotProbe)
                self.b.start()
                              
            
            if w :
                w.setupUi(dialog)
                dialog.exec_()
        


    def BotProbe(self, ip) :
        if  self.container_type != GenericContainer.CONTAINER_BOT :
            return
        if len(ip) > 0 :
            self.lw.addItem(ip)
        else :
            self.isProbing = False
            print 'isProbing is reset'



    def  RegisterContextMenuDialog(self,type,W) :
        GenericContainer.contextMenuDialogMap[type] = W
    


    @classmethod
    def FromFileStr(cls,jstring,sess=None) :
        d = json.loads(jstring)
        typ = d['type']
        o = None

        if typ == GenericContainer.TYPE_SSL_VSERVER  :
            o = SSLVServerEntity.FromFileStr(jstring,sess)
        elif typ == GenericContainer.TYPE_SSL_TCP_VSERVER  :
            pass
        elif typ == GenericContainer.TYPE_HTTP_VSERVER  :
            pass
        elif typ == GenericContainer.TYPE_TCP_VSERVER  :
            pass
        elif typ == GenericContainer.TYPE_SSL_SERVICE  :
            pass
        elif typ == GenericContainer.TYPE_SSL_TCP_SERVICE  :
            pass
        elif typ == GenericContainer.TYPE_HTTP_SERVICE  :
            pass
        elif typ == GenericContainer.TYPE_TCP_SERVICE  :
            pass
        elif typ == GenericContainer.TYPE_BE_OPENSSL_SERVER  :
            o = BEOpenSSLServerDialog.BEOpenSSLServerEntity.FromFileStr(jstring)
        elif typ == GenericContainer.TYPE_BE_APACHE_SERVER  :
            pass
        elif typ == GenericContainer.TYPE_BE_HTTP_DATA  :
            pass
        elif typ == GenericContainer.TYPE_FE_OPENSSL_CLIENT  :
            o = BasicClientEntity.FromFileStr(jstring)
        elif typ == GenericContainer.TYPE_FE_CURL_HTTPCLIENT  :
            pass
        elif typ == GenericContainer.TYPE_FE_CURL_SSL_CLIENT  :
            pass
        elif typ == GenericContainer.TYPE_FE_PIPELINE_SSL_CLIENT  :
            pass
        elif typ == GenericContainer.TYPE_OCSP_OPENSSL_SERVER  :
            o = OcspServerEntity.FromFileStr(jstring)
        elif typ == GenericContainer.TYPE_CRL_OPENSSL_SERVER  :
            pass

        return o






class BotProber(QtCore.QThread) :
    probeSig = QtCore.pyqtSignal(str)
    
    def __init__(self,subnet) :
        super(self.__class__,self).__init__()
        self.subnet = subnet

    def run(self) :
        for i in range(2,254) :
            ip = self.subnet + '.' + str(i)
            b = BasicClientEntity('basic',ip,2345,'1.1.1.1',1111)
            if b.Connect(timeout=0.3) :
                self.probeSig.emit(ip)
                b.Terminate()

        self.probeSig.emit('')





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
    Form.show()
    sys.exit(app.exec_())
    

