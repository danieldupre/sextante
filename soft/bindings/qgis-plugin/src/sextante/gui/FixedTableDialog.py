from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class FixedTableDialog(QtGui.QDialog):
    def __init__(self, param, table):
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.param = param
        self.rettable = table
        self.setupUi()
        self.rettable = None

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(600, 350)
        self.setWindowTitle("Fixed Table")
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(490, 10, 81, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(QtCore.QRect(10, 10, 470, 300))
        self.table.setObjectName("table")
        self.table.setColumnCount(len(self.param.cols))
        for i in range(len(self.param.cols)):
            self.table.setColumnWidth(i,380 / len(self.param.cols))
            self.table.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(self.param.cols[i]))
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table.setRowCount(len(self.rettable))
        for i in range(len(self.rettable)):
            self.table.setRowHeight(i,22)
        self.table.verticalHeader().setVisible(False)
        self.addRowButton = QtGui.QPushButton(self)
        self.addRowButton.setGeometry(QtCore.QRect(490, 290, 81, 23))
        self.addRowButton.setObjectName("addRowButton")
        self.addRowButton.setText("Add row")
        self.setTableContent()
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        QObject.connect(self.addRowButton, QtCore.SIGNAL("clicked()"), self.addRow)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setTableContent(self):
        for i in range(len(self.rettable)):
            for j in range(len(self.rettable[0])):
                self.table.setItem(i,j,QtGui.QTableWidgetItem(self.rettable[i][j]))

    def okPressed(self):
        self.rettable = []
        for i in range(self.table.rowCount()):
            self.rettable.append(list())
            for j in range(self.table.columnCount()):
                self.rettable[i].append(str(self.table.item(i,j).text()))
        self.close()

    def cancelPressed(self):
        self.rettable = None
        self.close()

    def addRow(self):
        self.table.setRowCount(self.table.rowCount()+1)
        self.table.setRowHeight(self.table.rowCount()-1, 22)
        for i in range(self.table.columnCount()):
            self.table.setItem(self.table.rowCount()-1,i,QtGui.QTableWidgetItem("0"))
