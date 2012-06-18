from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sextante.parameters.ParameterRaster import ParameterRaster
from sextante.parameters.ParameterTable import ParameterTable
from sextante.parameters.ParameterVector import ParameterVector
from sextante.gui.BatchInputSelectionPanel import BatchInputSelectionPanel
from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.parameters.ParameterSelection import ParameterSelection
from sextante.parameters.ParameterFixedTable import ParameterFixedTable
from sextante.gui.FixedTablePanel import FixedTablePanel
from sextante.parameters.ParameterMultipleInput import ParameterMultipleInput
import copy
from sextante.gui.BatchOutputSelectionPanel import BatchOutputSelectionPanel
from sextante.gui.AlgorithmExecutor import AlgorithmExecutor
from sextante.outputs.OutputHTML import OutputHTML
from sextante.core.SextanteResults import SextanteResults
from sextante.gui.ResultsDialog import ResultsDialog
from sextante.core.SextanteLog import SextanteLog

class BatchProcessingDialog(QtGui.QDialog):
    def __init__(self, alg):
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.alg = alg
        self.algs = None
        self.setupUi()
        self.algEx = None

    def setupUi(self):
        self.resize(800, 500)
        self.setWindowTitle("Batch Processing - " + self.alg.name)
        self.horizontalLayout = QtGui.QVBoxLayout(self)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setMargin(10)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.addRowButton = QtGui.QPushButton()
        self.addRowButton.setText("Add row")
        self.buttonBox.addButton(self.addRowButton, QtGui.QDialogButtonBox.ActionRole)
        self.deleteRowButton = QtGui.QPushButton()
        self.deleteRowButton.setText("Delete row")
        self.buttonBox.addButton(self.addRowButton, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.deleteRowButton, QtGui.QDialogButtonBox.ActionRole)
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(len(self.alg.parameters) + len(self.alg.outputs))
        self.setTableContent()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.progress = QtGui.QProgressBar()
        self.progress.setMinimum(0)
        self.horizontalLayout.addWidget(self.table)
        self.horizontalLayout.addWidget(self.progress)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.setLayout(self.horizontalLayout)
        QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        QObject.connect(self.addRowButton, QtCore.SIGNAL("clicked()"), self.addRow)
        QObject.connect(self.deleteRowButton, QtCore.SIGNAL("clicked()"), self.deleteRow)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setTableContent(self):
        i = 0
        for param in self.alg.parameters:
            self.table.setColumnWidth(i,250)
            self.table.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(param.description))
            i+=1
        for out in self.alg.outputs:
            self.table.setColumnWidth(i,250)
            self.table.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(out.description))
            i+=1

        for i in range(3):
            self.addRow()

    def okPressed(self):
        self.algs = []
        for row in range(self.table.rowCount()):
            alg = self.alg.getCopy()#copy.deepcopy(self.alg)
            col = 0
            for param in alg.parameters:
                widget = self.table.cellWidget(row, col)
                if not self.setParameterValueFromWidget(param, widget):
                    QMessageBox.critical(self.dialog, "Unable to execute batch process", "Wrong or missing parameter values")
                    self.algs = None
                    return
                col+=1
            for out in alg.outputs:
                widget = self.table.cellWidget(row, col)
                text = widget.getValue()
                if text.strip() != "":
                    out.value = text
                    col+=1
                else:
                    QMessageBox.critical(self, "Unable to execute batch process", "Wrong or missing parameter values")
                    self.algs = None
                    return
            self.algs.append(alg)

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.progress.setMaximum(len(self.algs))
        self.progress.setValue(0)
        self.nextAlg(0)

        self.table.setEnabled(False)

    def loadHTMLResults(self, alg, i):
        for out in alg.outputs:
            if out.hidden or not out.open:
                continue
            if isinstance(out, OutputHTML):
                SextanteResults.addResult(out.description + "[" + str(i) + "]", out.value)

    def cancelPressed(self):
        self.algs = None
        if self.algEx:
            self.algEx.terminate()
        self.close()

    @pyqtSlot()
    def finish(self, i):
        i += 1
        self.progress.setValue(i)
        if len(self.algs) == i:
            self.finishAll()
            self.algEx = None
        else:
            self.nextAlg(i)

    @pyqtSlot()
    def error(self, msg):
        QApplication.restoreOverrideCursor()
        QMessageBox.critical(self, "Error", msg)
        SextanteLog.addToLog(SextanteLog.LOG_ERROR, msg)
        self.close()

    def nextAlg(self, i):
        self.algEx = AlgorithmExecutor(self.algs[i]);
        self.algEx.error.connect(self.error)
        self.algEx.finished.connect(lambda: self.finish(i))
        self.algEx.start()

    def finishAll(self):
        i = 0
        for alg in self.algs:
            self.loadHTMLResults(alg, i)
            i = i + 1
        QApplication.restoreOverrideCursor()
        self.table.setEnabled(True)
        QMessageBox.information(self, "Batch processing", "Batch processing successfully completed!")
        self.close()

    def setParameterValueFromWidget(self, param, widget):
        if isinstance(param, (ParameterRaster, ParameterVector, ParameterTable, ParameterMultipleInput)):
            return param.setValue(widget.getText())
        elif isinstance(param, ParameterBoolean):
            return param.setValue(widget.currentIndex() == 0)
        elif isinstance(param, ParameterSelection):
            return param.setValue(widget.currentIndex())
        elif isinstance(param, ParameterFixedTable):
            return param.setValue(widget.table)
        else:
            return param.setValue(widget.text())

    def getWidgetFromParameter(self, param, row, col):
        if isinstance(param, (ParameterRaster, ParameterVector, ParameterTable, ParameterMultipleInput)):
            item = BatchInputSelectionPanel(param, row, col, self)
        elif isinstance(param, ParameterBoolean):
            item = QtGui.QComboBox()
            item.addItem("Yes")
            item.addItem("No")
            if param.default:
                item.setCurrentIndex(0)
            else:
                item.setCurrentIndex(1)
        elif isinstance(param, ParameterSelection):
            item = QtGui.QComboBox()
            item.addItems(param.options)
        elif isinstance(param, ParameterFixedTable):
            item = FixedTablePanel(param)
        else:
            item = QtGui.QLineEdit()
            try:
                item.setText(str(param.default))
            except:
                pass

        return item

    def deleteRow(self):
        if self.table.rowCount() > 2:
            self.table.setRowCount(self.table.rowCount()-1)

    def addRow(self):
        self.table.setRowCount(self.table.rowCount()+1)
        self.table.setRowHeight(self.table.rowCount()-1, 22)
        i=0
        for param in self.alg.parameters:
            self.table.setCellWidget(self.table.rowCount()-1,i, self.getWidgetFromParameter(param, self.table.rowCount()-1, i))
            i+=1
        for out in self.alg.outputs:
            self.table.setCellWidget(self.table.rowCount()-1,i, BatchOutputSelectionPanel(out, self.alg, self.table.rowCount()-1, i, self))
            i+=1
