import  sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSWidgets')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')


from   PyQt5 import QtCore, QtGui, QtWidgets
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver as LBVSERVER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver as SSLVSERVER
import nssrc.com.citrix.netscaler.nitro.exception.nitro_exception as NITROEXCEPTION
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey as CERTKEY
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcipher as CIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslciphersuite as CIPHERSUITE
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcipher_binding as SSLVSRVRCIPHER
import nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslciphersuite_binding as SSLVSRVRCIPHERSUITE
import nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding as LBVSRVRSVC



import GenericContainer
import CertInstaller
import test_util
import CustomWidget
import json


class HttpVServerDialog(object):
    def  __init__(self,container = None) :
        self.container = container
        self.curDUT = container.GetCurDUT()

    def setupUi(self, dialog):
        self.dialog = dialog
        dialog.setObjectName("HttpVServerDialog")
        dialog.resize(100, 200)

        dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.topGrid = QtWidgets.QGridLayout(dialog)
        self.topGrid.setObjectName("topGrid")

        self.lineEdit_name = QtWidgets.QLineEdit(dialog)
        self.lineEdit_name.setAccessibleName("")
        self.lineEdit_name.setAccessibleDescription("")
        self.lineEdit_name.setText("")
        self.lineEdit_name.setObjectName("lineEdit_name")

        self.lineEdit_ip = QtWidgets.QLineEdit(dialog)
        self.lineEdit_ip.setObjectName("lineEdit_ip")

        self.lineEdit_port = QtWidgets.QLineEdit(dialog)
        self.lineEdit_port.setObjectName("lineEdit_port")

        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")

        self.topGrid.addWidget(self.lineEdit_name,   0,0,1,1)
        self.topGrid.addWidget(self.lineEdit_ip,     0,1,1,1)
        self.topGrid.addWidget(self.lineEdit_port,   0,2,1,1)
        self.topGrid.addWidget(self.buttonBox, 2,0,1,1)


        self.retranslateUi(dialog)
        self.buttonBox.rejected.connect(self.dialog.reject)


        self.retranslateUi(dialog)
        self.buttonBox.rejected.connect(self.dialog.reject)

        if (self.container.GetType() == GenericContainer.GenericContainer.TYPE_HTTP_VSERVER):
            self.buttonBox.accepted.connect(self.acceptSave)
            obj = self.container.GetBackendObj()
            if  obj :
                self.curDUT = self.GetDUTByIP(obj.nsip)
                self.FillFromObj(obj)
        else :
            self.buttonBox.accepted.connect(self.accept)


    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "dialog"))
        
        self.lineEdit_port.setPlaceholderText(_translate("dialog", "Port"))
        self.lineEdit_ip.setPlaceholderText(_translate("dialog", "IP"))
        self.lineEdit_name.setPlaceholderText(_translate("dialog", "Name"))


    def GetSess(self) :
        return self.curDUT.sess


    def GetCurDUT(self) :
        return self.curDUT


    def GetDUTByIP(self,nsip) :
        return self.container.GetDUTByIP(nsip)



    def FormSanity(self) :
        try :
            ersacount = int(self.lineEdit_port.text())
        except ValueError as e :
            return False
        return True


    def UpdateEntity(self, obj) :
        return True


    def accept(self) :
        if not self.FormSanity() :
            return

        try :
            self.curDUT.sess.relogin()
            e = self.BuildEntity()
            if not e :
                print 'entity creation failed'
                return
            
            if not self.UpdateEntity(e) :
                print 'accept failure (update failed)'
                e.Delete()
                return
            
            ew = self.container.AddEntity(e.entity_type)
            ew.SetBackendObj(e)
            self.dialog.accept()
            return

        except NITROEXCEPTION as e :
            plt = self.lineedit_name.palette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            plt.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.lineedit_name.setPalette(plt)
            self.lineedit_name.cursorPositionChanged.connect(self.cursorPositionChanged)
            return
        except Exception as e :
            print 'Vserver creation failed: {}'.format(e.message)
            return


    def acceptSave(self) :
        if not self.FormSanity() :
            return
        obj = self.container.GetBackendObj()
        self.UpdateEntity(obj)
        self.dialog.accept()



    def FillFromObj(self,obj) :
        if obj.fromfiledict :
            self.FillFromDict(obj.fromfiledict)
            obj.fromfiledict = None
            return
        
        self.lineEdit_name.setText(obj.name)
        self.lineEdit_ip.setText(obj.ip)
        self.lineEdit_port.setText(str(obj.port))



    def FillFromDict(self,d) :
        self.lineEdit_name.setText(d['name'])
        self.lineEdit_ip.setText(d['ip'])
        self.lineEdit_port.setText(str(d['port']))


    def BuildEntity(self) :
        name = self.lineEdit_name.text()
        ip   = self.lineEdit_ip.text()
        port = int(self.lineEdit_port.text())
        sess = self.curDUT.sess

        dut = self.GetCurDUT()
        obj = HttpVServerEntity(name,ip,port,'HTTP',sess, dut.nsip);
        if not obj.Create() :
            print 'Failed to add LB Vserver'
            return None
        
        return obj







class HttpVServerEntity (QtCore.QObject):
    sigStatus = QtCore.pyqtSignal(int)
    
    def __init__(self,name,ip,port,vtype,sess,nsip=None) :
        super(self.__class__,self).__init__()
        self.name  = name
        self.ip    = ip
        self.port  = port
        self.type  = vtype
        self.lb = None
        self.sess = sess
        self.nsip = nsip
        self.isrunning = False
        self.fromfiledict = None
        self.entity_type = GenericContainer.GenericContainer.TYPE_HTTP_VSERVER


    def IsRunning(self) :
        return self.isrunning

    def IsStartStop(self) :
        return False
    
    def IsResults(self) :
        return False

    def IsProperty(self) :
        return True

    def GetType(self) :
        return self.entity_type


    def UpDownSlot(self, i) :
        if i > 0 :
            self.isRunning = True
        else :
            self.isRunning = False


    def Refresh(self) :
        try :
            if self.lb :
                self.lb  = LBVSERVER.lbvserver.get(self.sess,self.name)
        except NITROEXCEPTION as e :
            print 'HttpVserverEntity:Refresh: NitroException{}'.format(e.message)
            self.lb = None
            print '{}'.format(e.message)
        except Exception as e :
            print 'HttpVserverEntity:Refresh Exception {}'.format(e.message)
            self.lb = None

        if self.lb :
            if self.lb.curstate == 'UP' :
                self.isrunning = True
            else :
                self.isrunning = False



    def GetName(self) :
        name = self.name + '\n' + self.ip + '\n' + str(self.port)
        return name


    def Create(self) :
        httpv = LBVSERVER.lbvserver()
        httpv.name = self.name
        httpv.servicetype = self.type
        httpv.port = self.port
        httpv.ipv46 = self.ip

        try :
            self.lb  = LBVSERVER.lbvserver.add(self.sess,httpv)
        except NITROEXCEPTION as e :
            self.lb = None
            print '{}'.format(e.message)
        except Exception as e :
            self.lb = None
            print '{}'.format(e.message)

        return self.lb



    def Delete(self) :
        httpv = LBVSERVER.lbvserver()
        httpv.name = self.name
        httpv.servicetype = self.type
        httpv.port = self.port
        httpv.ipv46 = self.ip

        try :
            LBVSERVER.lbvserver.delete(self.sess,httpv)
        except NITROEXCEPTION as e :
            self.lb = None
            print '{}'.format(e.message)
        except Exception as e :
            self.lb = None
            print '{}'.format(e.message)




    def ToJson(self) :
        d = dict()
        d['name'] = self.name
        d['ip'] = self.ip
        d['nsip'] = self.nsip
        d['port']  = self.port
        d['type']  = self.type

        s = json.dumps(d)
        return s


    def ToFileStr(self) :
        js = self.ToJson()
        d = dict()
        d['type'] = self.entity_type
        d['val'] = js
        s = json.dumps(d)
        return s


    @classmethod
    def FromFileStr(cls,jstring,sess=None) :
        d = json.loads(jstring)
        d = json.loads(d['val'])
        nsip = d['nsip']

        try :
            lb = LBVSERVER.lbvserver.get(sess,d['name'])
            if(lb) :
                LBVSERVER.lbvserver.delete(sess,lb)
        except NITROEXCEPTION as e :
            pass
        except Exception as e :
            pass
        
        obj = HttpVServerEntity(d['name'],d['ip'],d['port'],d['type'],sess,nsip)
        obj.fromfiledict = d
    
        if not obj.Create() :
            print 'obj.Create() failed'
            return None

        return obj


    def AllowDrop(self,jstring) :
        d = json.loads(jstring)
        t = d['type']
        if ((t == GenericContainer.GenericContainer.TYPE_SSL_SERVICE) or (t == GenericContainer.GenericContainer.TYPE_HTTP_SERVICE)):
            return True
        else :
            return False
        

    def HandleDropEvent(self,jstring) :
        d = json.loads(jstring)
        svcname = d['name']
        bndg = LBVSRVRSVC.lbvserver_service_binding()
        bndg.name = self.name
        bndg.servicename = svcname

        try :
            LBVSRVRSVC.lbvserver_service_binding.add(self.sess,bndg)
        except NITROEXCEPTION as e :
            print 'service drop failed'
        except Exception as e :
            print 'service drop failed'
        
        return





    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    container = GenericContainer.GenericContainer(GenericContainer.GenericContainer.TYPE_HTTP_VSERVER)
    ui = HttpVServerDialog(container)
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())


