# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basic_server.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\NSPY')
sys.path.append('C:\\Users\\ashokes\\Miniconda2\\ashoke-miniconda2\\nitro-python-1.0')

from PyQt5 import QtCore, QtGui, QtWidgets
from   guiValidation    import *


class Ui_basic_server_form(object):
    def __init__(self) :
        self.beserver_list = []
        self.pth = PollThread(self)
        #self.pth.start()
        
    
    def setupUi(self, basic_server_form):
        basic_server_form.setObjectName("basic_server_form")
        #basic_server_form.resize(612, 527)
        basic_server_form.resize(90, 527)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(basic_server_form.sizePolicy().hasHeightForWidth())
        basic_server_form.setSizePolicy(sizePolicy)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(basic_server_form)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.master_widget = QtWidgets.QWidget(basic_server_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.master_widget.sizePolicy().hasHeightForWidth())
        self.master_widget.setSizePolicy(sizePolicy)
        self.master_widget.setObjectName("master_widget")
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.master_widget)
        self.horizontalLayout_2.setContentsMargins(2, 0, 6, 0)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.server_config = QtWidgets.QWidget(self.master_widget)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.server_config.sizePolicy().hasHeightForWidth())
        self.server_config.setSizePolicy(sizePolicy)
        self.server_config.setObjectName("server_config")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.server_config)
        #self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")

        self.le_name = QtWidgets.QLineEdit(self.server_config)
        self.le_name.setStyleSheet("border-color: rgb(44, 44, 44);")
        self.le_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.le_name.setObjectName("le_name")
        self.verticalLayout.addWidget(self.le_name)
        spacerItem = QtWidgets.QSpacerItem(40, 4, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)

        self.le_ip = QtWidgets.QLineEdit(self.server_config)
        self.le_ip.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.le_ip.setObjectName("le_ip")
        self.verticalLayout.addWidget(self.le_ip)
        spacerItem1 = QtWidgets.QSpacerItem(40, 4, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)

        self.le_listen_port = QtWidgets.QLineEdit(self.server_config)
        self.le_listen_port.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.le_listen_port.setObjectName("le_listen_port")
        self.verticalLayout.addWidget(self.le_listen_port)
        spacerItem2 = QtWidgets.QSpacerItem(40, 4, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)

        self.le_resp_size = QtWidgets.QLineEdit(self.server_config)
        self.le_resp_size.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.le_resp_size.setObjectName("le_resp_size")
        self.verticalLayout.addWidget(self.le_resp_size)
        spacerItem3 = QtWidgets.QSpacerItem(40, 4, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)

        self.le_record_size = QtWidgets.QLineEdit(self.server_config)
        self.le_record_size.setObjectName("le_record_size")
        self.verticalLayout.addWidget(self.le_record_size)
        spacerItem4 = QtWidgets.QSpacerItem(40, 4, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem4)

        self.le_cipher_filter = QtWidgets.QLineEdit(self.server_config)
        self.le_cipher_filter.setObjectName("le_cipher_filter")
        self.verticalLayout.addWidget(self.le_cipher_filter)
        spacerItem5 = QtWidgets.QSpacerItem(40, 4, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)

        self.cb_reuse = QtWidgets.QCheckBox(self.server_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_reuse.sizePolicy().hasHeightForWidth())
        self.cb_reuse.setSizePolicy(sizePolicy)
        self.cb_reuse.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cb_reuse.setTristate(False)
        self.cb_reuse.setObjectName("cb_reuse")
        self.verticalLayout.addWidget(self.cb_reuse)
        self.cb_reneg = QtWidgets.QCheckBox(self.server_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_reneg.sizePolicy().hasHeightForWidth())
        self.cb_reneg.setSizePolicy(sizePolicy)
        self.cb_reneg.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cb_reneg.setObjectName("cb_reneg")
        self.verticalLayout.addWidget(self.cb_reneg)
        self.cb_cauth = QtWidgets.QCheckBox(self.server_config)
        self.cb_cauth.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cb_cauth.setObjectName("cb_cauth")
        self.verticalLayout.addWidget(self.cb_cauth)

        self.button_panel = QtWidgets.QWidget(self.server_config)
        self.button_panel.setObjectName("button_panel")
        self.gridLayout = QtWidgets.QGridLayout(self.button_panel)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_save = QtWidgets.QPushButton(self.button_panel)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout.addWidget(self.btn_save, 0, 0, 1, 1)
        self.btn_discard = QtWidgets.QPushButton(self.button_panel)
        self.btn_discard.setObjectName("btn_discard")
        self.gridLayout.addWidget(self.btn_discard, 0, 1, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self.button_panel)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout.addWidget(self.btn_stop, 1, 1, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self.button_panel)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout.addWidget(self.btn_start, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.button_panel)

        self.btn_save.clicked.connect(self.btn_save_slot)
        self.btn_discard.clicked.connect(self.btn_discard_slot)
        self.btn_start.clicked.connect(self.btn_start_slot)
        self.btn_stop.clicked.connect(self.btn_stop_slot)
        

        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem6)
        self.server_list = QtWidgets.QListWidget(self.server_config)
        self.server_list.setObjectName("server_list")
        self.verticalLayout.addWidget(self.server_list)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(6, 1)
        self.verticalLayout.setStretch(14, 1)
        self.horizontalLayout_2.addWidget(self.server_config)

        #self.server_status = QtWidgets.QTextEdit(self.master_widget)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #sizePolicy.setHorizontalStretch(2)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.server_status.sizePolicy().hasHeightForWidth())
        #self.server_status.setSizePolicy(sizePolicy)
        #self.server_status.setStyleSheet("border-color: rgb(250, 250, 250);\n"
#"background-color: rgb(255, 255, 255);\n"
#"background-color: rgb(49, 49, 49);")
        #self.server_status.setObjectName("server_status")
        #self.horizontalLayout_2.addWidget(self.server_status)

        self.horizontalLayout.addWidget(self.master_widget)

        self.server_list.itemClicked.connect(self.DisplaySelected)

        self.retranslateUi(basic_server_form)
        QtCore.QMetaObject.connectSlotsByName(basic_server_form)



    def retranslateUi(self, basic_server_form):
        _translate = QtCore.QCoreApplication.translate
        #basic_server_form.setWindowTitle(_translate("basic_server_form", "Server Setting"))
        basic_server_form.setWindowTitle(_translate("basic_server_form", "Server"))
        self.le_name.setPlaceholderText(_translate("basic_server_form", "Server Name"))
        self.le_ip.setPlaceholderText(_translate("basic_server_form", "Server IP"))
        self.le_listen_port.setPlaceholderText(_translate("basic_server_form", "Server Listen Port"))
        self.le_resp_size.setPlaceholderText(_translate("basic_server_form", "Response Size"))
        self.le_record_size.setPlaceholderText(_translate("basic_server_form", "Record Size"))
        self.le_cipher_filter.setPlaceholderText(_translate("basic_server_form", "Cipher Filter"))
        self.cb_reuse.setText(_translate("basic_server_form", "Reuse"))
        self.cb_reneg.setText(_translate("basic_server_form", "Reneg"))
        self.cb_cauth.setText(_translate("basic_server_form", "CAuth"))
        self.btn_save.setText(_translate("basic_server_form", "Save"))
        self.btn_discard.setText(_translate("basic_server_form", "Discard"))
        self.btn_stop.setText(_translate("basic_server_form", "Stop"))
        self.btn_start.setText(_translate("basic_server_form", "Start"))


    def btn_save_slot(self, checked) :
        #print 'btn_save_slot ...'
        name = self.le_name.text()
        b = self.CreateBEServer()
        if not b :
            print 'No such server {}'.format(name)
            return False
        
        if not b.sd :
            if not b.Connect() :
                print 'Failed to connect to {}'.format(name)
                b.sd = None
                return False

        str = self.ServerToJSon()
        lstr = struct.pack(">I", len(str))
        b.sd.sendall(lstr)
        b.sd.sendall(str)

        if not self.pth.isRunning() :
            self.pth.start()
        
        return True



    def btn_discard_slot(self, checked) :
        #print 'btn_discard_slot ...'
        self.RemoveSelected()
        self.ClearDisplay()


    def btn_start_slot(self,checked) :
        name = self.le_name.text()
        beS = self.FindBESByName(name)
        if not beS :
            print 'No such server {}'.format(name)
            return False

        if not beS.sd :
            if not beS.Connect() :
                print 'Failed to connect to {}'.format(name)
                beS.sd = None
                return False
            
        str = self.ServerToJSon()
        lstr = struct.pack(">I", len(str))
        beS.sd.sendall(lstr)
        beS.sd.sendall(str)

        if not self.pth.isRunning() :
            self.pth.start()
        
        return True


    def btn_stop_slot(self, checked) :
        #print 'btn_stop_slot ...'
        name = self.le_name.text()
        beS = self.FindBESByName(name)
        if not beS :
            print 'No such server {}'.format(name)
            return False

        if beS.sd :
            beS.SendClose()

        return True

    




    def CreateBEServer(self) :
        name = None
        ip = None
        listen_port = None
        resp_size = None
        record_size = None
        cipher_filter = None

        try :
            name = self.le_name.text()
            ip = self.le_ip.text()
            listen_port = int(self.le_listen_port.text())
            resp_size = int(self.le_resp_size.text())
            record_size = int(self.le_record_size.text())
            cipher_filter = self.le_cipher_filter.text()

        except ValueError as e :
            pass

        if(self.cb_reuse.isChecked() == True) :
            reuse = True
        else :
            reuse = False
            
        if(self.cb_reneg.isChecked() == True) :
            reneg = True
        else:
            reneg = False
        
        if(self.cb_cauth.isChecked() == True) :
            cauth = True
        else :
            cauth = False


        b = self.FindBESByName(name)
        if not b :
            b = BEServer(name,ip,listen_port,resp_size,record_size,cipher_filter,reuse,reneg,cauth)
            self.AddBEServer(b)
        else :
            b.ip = ip
            b.listen_port = listen_port
            b.resp_size = resp_size
            b.rec_size = record_size
            b.cipher_filter = cipher_filter
            b.reuse = reuse
            b.reneg = reneg
            b.cauth = cauth
            
        return b



    def ServerToJSon(self) :
        d = dict()
        d['listen_port'] =  self.le_listen_port.text()
        d['resp_size'] = self.le_resp_size.text()
        d['record_size'] = self.le_record_size.text()
        d['cipher_filter'] = self.le_cipher_filter.text()
        d['reuse'] = self.cb_reuse.isChecked()
        d['reneg'] = self.cb_reneg.isChecked()
        d['cauth'] =  self.cb_cauth.isChecked()
        
        s = json.dumps(d)
        #print s
        return s
    

    def AddBEServer(self,beS) :
        ret = True
        for b in self.beserver_list :
            if beS.name == b.name :
                ret = False
                break

        if ret :
            self.server_list.addItem(beS.name)
            self.beserver_list.append(beS)
        return ret



    def FindBESByName(self,name) :
        for b in self.beserver_list :
            if name == b.name :
                return b

        return None


    def RemoveSelected(self) :
        row  = self.server_list.currentRow()
        name = self.server_list.item(row).text()

        for b in self.beserver_list :
            if b.name == name :
                self.beserver_list.remove(b)
                break
        
        self.server_list.takeItem(row)
        



    def DisplayItem(self, item) :
        self.le_name.setText(item.name)
        self.le_ip.setText(item.ip)
        self.le_listen_port.setText(str(item.listen_port))
        self.le_resp_size.setText(str(item.resp_size))
        self.le_record_size.setText(str(item.rec_size))

        if(item.reuse) :
            self.cb_reuse.setCheckState(2)
        else :
            self.cb_reuse.setCheckState(0)

        if(item.reneg) :
            self.cb_reneg.setCheckState(2)
        else :
            self.cb_reneg.setCheckState(0)
    
        if(item.cauth) :
            self.cb_cauth.setCheckState(2)
        else :
            self.cb_cauth.setCheckState(0)



    def ClearDisplay(self) :
        self.le_name.setText('')
        self.le_ip.setText('')
        self.le_listen_port.setText('')
        self.le_resp_size.setText('')
        self.le_record_size.setText('')

        self.cb_reuse.setCheckState(0)
        self.cb_reneg.setCheckState(0)
        self.cb_cauth.setCheckState(0)






    def DisplaySelected(self, s) :
        b = None
        row  = self.server_list.currentRow()
        name = self.server_list.item(row).text()
        for b in self.beserver_list :
            if b.name == name :
                break

        if b :
            self.DisplayItem(b)

    
            
            
        
        


class   BEServer(object) :
    def __init__(self,name,ip=None,listen_port=None,resp_size=None,rec_size=None,cipher_filter=None,reuse=False,reneg=False,cauth=False) :
        self.name = name
        self.ip = ip
        self.listen_port = listen_port
        self.resp_size = resp_size
        self.rec_size = rec_size
        self.cipher_filter = cipher_filter
        self.reuse = reuse
        self.reneg = reneg
        self.cauth = cauth
        self.sd = None


    def Connect(self, timeout=2.0) :
        ret = True
        try :
            self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sd.settimeout(timeout)
            self.sd.connect ((self.ip, 2347))

            str = 'twinkletwinkle'
            lstr = struct.pack(">I", len(str))
            self.sd.sendall(lstr)
            self.sd.sendall(str)

            data = self.ReadOnce()
            if not data :
                ret = False
                return ret

            #print 'data read {}'.format(data)
            if not data.__eq__('howiwonder'):
                ret = False
                return ret
            
        except socket.error as e :
            ret = False

        #print 'connect returning {}'.format(ret)
        return ret


    def  ReadOnce(self) :
        try :
            data = self.sd.recv(4)
        except  socket.error as e  :
            data = None
        
        if not data :
            return None

        len = struct.unpack("<I",data)
        if(len[0] == 0) :
            return None

        #print 'ReadOnce len {}'.format(len[0])
        data = self.sd.recv(len[0])
        return data


    def  PollOnce(self) :
        #print 'PollOnce for {}'.format(self.name)
        if not self.sd :
            #print 'PollOnce: no sd'
            return None
    
        tout = self.sd.gettimeout()
        self.sd.settimeout(0.0)
        data = self.ReadOnce()
        self.sd.settimeout(tout)
        if data :
            print data
        else :
            pass
            #print 'PollOnce no data'
        
        return data


    def SendClose(self) :
        str = ''
        lstr = struct.pack(">I", len(str))
        self.sd.sendall(lstr)
        self.sd.close()
        self.sd = None






class PollThread(QtCore.QThread) :
    def __init__(self, ctx) :
        super(PollThread,self).__init__()
        self.ctx = ctx
        self.contd = True

    def  run(self) :
        while self.contd :
            for beS in self.ctx.beserver_list :
                beS.PollOnce()

            time.sleep(1.0)


            

    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    basic_server_form = QtWidgets.QWidget()
    ui = Ui_basic_server_form()
    ui.setupUi(basic_server_form)
    basic_server_form.show()
    sys.exit(app.exec_())

