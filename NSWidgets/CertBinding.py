# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CertBinding.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class CertBindingDialog(object):
    def __init__(self,entity) :
        self.entity = entity

    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(513, 324)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")


        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        

        self.server_cert = ListWidgetDD(1,self.widget)
        self.server_cert.setObjectName("server_cert")
        self.server_cert.setAcceptDrops(True)
        self.server_cert.setDragEnabled(True)
        self.verticalLayout.addWidget(self.server_cert)
      
        self.sni_cert = ListWidgetDD(0,self.widget)
        self.sni_cert.setAcceptDrops(True)
        self.sni_cert.setObjectName("sni_cert")
        self.sni_cert.setAcceptDrops(True)
        self.sni_cert.setDragEnabled(True)
        self.verticalLayout.addWidget(self.sni_cert)
        
        self.ca_cert = ListWidgetDD(0,self.widget)
        self.ca_cert.setAcceptDrops(True)
        self.ca_cert.setObjectName("ca_cert")
        self.ca_cert.setAcceptDrops(True)
        self.ca_cert.setDragEnabled(True)
        self.verticalLayout.addWidget(self.ca_cert)
        

        
        self.listwidget_certlist = QtWidgets.QListWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_certlist.sizePolicy().hasHeightForWidth())
        self.listwidget_certlist.setSizePolicy(sizePolicy)
        self.listwidget_certlist.setObjectName("listwidget_certlist")

        item = QtWidgets.QListWidgetItem()
        self.listwidget_certlist.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listwidget_certlist.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listwidget_certlist.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listwidget_certlist.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listwidget_certlist.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listwidget_certlist.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listwidget_certlist.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listwidget_certlist.addItem(item)
        self.listwidget_certlist.setDragEnabled(True)

        self.horizontalLayout.addWidget(self.widget)
        self.horizontalLayout.addWidget(self.listwidget_certlist)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        __sortingEnabled = self.listwidget_certlist.isSortingEnabled()
        self.listwidget_certlist.setSortingEnabled(False)

        item = self.listwidget_certlist.item(0)
        item.setText(_translate("Form", "One"))
        item = self.listwidget_certlist.item(1)
        item.setText(_translate("Form", "Two"))
        item = self.listwidget_certlist.item(2)
        item.setText(_translate("Form", "Three"))
        item = self.listwidget_certlist.item(3)
        item.setText(_translate("Form", "Four"))
        item = self.listwidget_certlist.item(4)
        item.setText(_translate("Form", "Five"))
        item = self.listwidget_certlist.item(5)
        item.setText(_translate("Form", "Six"))
        item = self.listwidget_certlist.item(6)
        item.setText(_translate("Form", "Seven"))
        item = self.listwidget_certlist.item(7)
        item.setText(_translate("Form", "Eight"))
        self.listwidget_certlist.setSortingEnabled(__sortingEnabled)






class ListWidgetDD(QtWidgets.QListWidget) :
    
    def __init__(self,maxe,parent) :
        self.certList = []
        self.maxe = maxe
        super(ListWidgetDD, self).__init__(parent)


    def dragEnterEvent(self,e) :
        if self.maxe > 0 :
            if self.count() >= self.maxe :
                return
        md = e.mimeData()
        mdata = md.data('application/x-qabstractitemmodeldatalist')
        data = self.decode_data(mdata)
        if data in self.certList :
            return
        super(ListWidgetDD, self).dragEnterEvent(e)


    def contextMenuEvent(self, event) :
        menu = QtWidgets.QMenu(self)
        actD = menu.addAction('Delete')
        act = menu.exec_(event.globalPos())
        if act == actD :
            r = self.currentRow()
            s = self.item(r).text()
            self.takeItem(r)
            self.certList.remove(s)
            


    def dropMimeData(self,index,data,action) :
        ret = super(ListWidgetDD, self).dropMimeData(index,data,action)
        i = self.item(index)
        self.certList.append(i.text())
        return ret


    def decode_data(self, mdata):
    
        data = []
        item = {}
        
        ds = QtCore.QDataStream(mdata)
        while not ds.atEnd():
        
            row = ds.readInt32()
            column = ds.readInt32()
            
            map_items = ds.readInt32()
            for i in range(map_items):
            
                key = ds.readInt32()
                
                value = QtCore.QVariant()
                ds >> value
                #item[Qt.ItemDataRole(key)] = value
                item[QtCore.Qt.ItemDataRole(key)] = value
            
            data.append(item)
        
        return data[0][0].value()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = CertBindingDialog(1)
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

