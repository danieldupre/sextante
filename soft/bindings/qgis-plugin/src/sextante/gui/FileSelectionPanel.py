from PyQt4 import QtGui, QtCore
from sextante.core.SextanteUtils import SextanteUtils

class FileSelectionPanel(QtGui.QWidget):

    def __init__(self):
        super(FileSelectionPanel, self).__init__(None)
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.text = QtGui.QLineEdit()
        self.text.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout.addWidget(self.text)
        self.pushButton = QtGui.QPushButton()
        self.pushButton.setText("...")
        self.pushButton.clicked.connect(self.showSelectionDialog)
        self.horizontalLayout.addWidget(self.pushButton)
        self.setLayout(self.horizontalLayout)

    def showSelectionDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Open file", QtCore.QString(""), "*.*")
        if filename:
            self.text.setText(str(filename))

    def getValue(self):
        s = str(self.text.text())
        if SextanteUtils.isWindows():
            s = s.replace("/", "\\")
        return s
