#!/usr/bin/env python
# -*- coding: latin-1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, QtWebKit
from sextante.core.QGisLayers import QGisLayers
from sextante.parameters.ParameterRaster import ParameterRaster
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.parameters.ParameterSelection import ParameterSelection
from sextante.parameters.ParameterMultipleInput import ParameterMultipleInput
from sextante.parameters.ParameterFixedTable import ParameterFixedTable
from sextante.parameters.ParameterTableField import ParameterTableField
from sextante.parameters.ParameterTable import ParameterTable
from sextante.gui.AlgorithmExecutor import AlgorithmExecutor
from sextante.core.SextanteLog import SextanteLog
from sextante.gui.SextantePostprocessing import SextantePostprocessing
from sextante.parameters.ParameterRange import ParameterRange
from sextante.parameters.ParameterNumber import ParameterNumber

from sextante.gui.ParametersPanel import ParametersPanel
from sextante.parameters.ParameterFile import ParameterFile
from sextante.parameters.ParameterCrs import ParameterCrs
from sextante.core.SextanteConfig import SextanteConfig
from sextante.parameters.ParameterExtent import ParameterExtent
from sextante.outputs.OutputHTML import OutputHTML
from sextante.outputs.OutputRaster import OutputRaster
from sextante.outputs.OutputVector import OutputVector
from sextante.outputs.OutputTable import OutputTable
from sextante.core.WrongHelpFileException import WrongHelpFileException
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class ParametersDialog(QtGui.QDialog):
    '''the default parameters dialog, to be used when an algorithm is called from the toolbox'''
    def __init__(self, alg):
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.ui = Ui_ParametersDialog()
        self.ui.setupUi(self, alg)
        self.executed = False

class Ui_ParametersDialog(object):

    NOT_SELECTED = "[Not selected]"

    def setupUi(self, dialog, alg):
        self.alg = alg
        self.dialog = dialog
        dialog.resize(650, 450)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setEnabled(False)

        self.paramTable = ParametersPanel(self.alg, self.dialog)
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidget(self.paramTable)
        self.scrollArea.setWidgetResizable(True)
        dialog.setWindowTitle(self.alg.name)
        self.progressLabel = QtGui.QLabel()
        self.progress = QtGui.QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.verticalLayout = QtGui.QVBoxLayout(dialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.setMinimumWidth(300)
        self.tabWidget.addTab(self.scrollArea, "Parameters")
        self.verticalLayout.addWidget(self.tabWidget)
        self.webView = QtWebKit.QWebView()
        cssUrl = QtCore.QUrl(os.path.join(os.path.dirname(__file__), "help", "help.css"))
        self.webView.settings().setUserStyleSheetUrl(cssUrl)
        html = None
        try:
            if self.alg.helpFile():
                helpFile = self.alg.helpFile()
            else:
                html = "<h2>Sorry, no help is available for this algorithm.</h2>"
        except WrongHelpFileException, e:
            html = e.msg
            self.webView.setHtml("<h2>Could not open help file :-( </h2>")
        try:
            if html:
                self.webView.setHtml(html)
            else:
                url = QtCore.QUrl(helpFile)
                self.webView.load(url)
        except:
            self.webView.setHtml("<h2>Could not open help file :-( </h2>")
        self.tabWidget.addTab(self.webView, "Help")
        self.verticalLayout.addWidget(self.progressLabel)
        self.verticalLayout.addWidget(self.progress)
        self.verticalLayout.addWidget(self.buttonBox)
        dialog.setLayout(self.verticalLayout)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.dialog.close)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.cancel)
        QtCore.QMetaObject.connectSlotsByName(dialog)


    def setParamValues(self):
        params = self.alg.parameters
        outputs = self.alg.outputs

        for param in params:
            if not self.setParamValue(param, self.paramTable.valueItems[param.name]):
                return False

        for output in outputs:
            if output.hidden:
                continue
            output.value = self.paramTable.valueItems[output.name].getValue()
            if not SextanteConfig.getSetting(SextanteConfig.TABLE_LIKE_PARAM_PANEL):
                if isinstance(output, (OutputRaster, OutputVector, OutputTable, OutputHTML)):
                    output.open = self.paramTable.checkBoxes[output.name].isChecked()

        return True

    def setParamValue(self, param, widget):
        if isinstance(param, ParameterRaster):
            return param.setValue(widget.getValue())
        elif isinstance(param, (ParameterVector, ParameterTable)):
            try:
                return param.setValue(widget.itemData(widget.currentIndex()).toPyObject())
            except:
                return param.setValue(widget.getValue())
        elif isinstance(param, ParameterBoolean):
            return param.setValue(widget.currentIndex() == 0)
        elif isinstance(param, ParameterSelection):
            return param.setValue(widget.currentIndex())
        elif isinstance(param, ParameterFixedTable):
            return param.setValue(widget.table)
        elif isinstance(param, ParameterRange):
            return param.setValue(widget.getValue())
        if isinstance(param, ParameterTableField):
            return param.setValue(widget.currentText())
        elif isinstance(param, ParameterMultipleInput):
            if param.datatype == ParameterMultipleInput.TYPE_VECTOR_ANY:
                options = QGisLayers.getVectorLayers()
            else:
                options = QGisLayers.getRasterLayers()
            value = []
            for index in widget.selectedoptions:
                value.append(options[index])
            return param.setValue(value)
        elif isinstance(param, (ParameterNumber, ParameterFile, ParameterCrs, ParameterExtent)):
            return param.setValue(widget.getValue())
        else:
            return param.setValue(str(widget.text()))

    @pyqtSlot()
    def accept(self):
        #~ try:
        if self.setParamValues():
            msg = self.alg.checkParameterValuesBeforeExecuting()
            if msg:
                QMessageBox.critical(self.dialog, "Unable to execute algorithm", msg)
                return
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
            self.buttonBox.button(QtGui.QDialogButtonBox.Close).setEnabled(False)
            buttons = self.paramTable.iterateButtons
            iterateParam = None

            for i in range(len(buttons.values())):
                button = buttons.values()[i]
                if button.isChecked():
                    iterateParam = buttons.keys()[i]
                    break

            self.progress.setMaximum(0)
            self.progressLabel.setText("Processing algorithm...")
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            if iterateParam:
                self.algEx = AlgorithmExecutor(self.alg, iterateParam)
            else:
                command = self.alg.getAsCommand()
                if command:
                    SextanteLog.addToLog(SextanteLog.LOG_ALGORITHM, command)
                self.algEx = AlgorithmExecutor(self.alg)
            self.algEx.finished.connect(self.finish)
            self.algEx.error.connect(self.error)
            self.algEx.percentageChanged.connect(self.setPercentage)
            self.algEx.textChanged.connect(self.setText)
            self.algEx.start()
            self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setEnabled(True)
        else:
            QMessageBox.critical(self.dialog, "Unable to execute algorithm", "Wrong or missing parameter values")

    @pyqtSlot()
    def finish(self):
        self.dialog.executed = True
        QApplication.restoreOverrideCursor()
        keepOpen = SextanteConfig.getSetting(SextanteConfig.KEEP_DIALOG_OPEN)
        if not keepOpen:
            self.dialog.close()
        else:
            self.progressLabel.setText("")
            self.progress.setMaximum(100)
            self.progress.setValue(0)
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
            self.buttonBox.button(QtGui.QDialogButtonBox.Close).setEnabled(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setEnabled(False)
        SextantePostprocessing.handleAlgorithmResults(self.alg, not keepOpen)

    @pyqtSlot()
    def error(self, msg):
        self.algEx.finished.disconnect()
        QApplication.restoreOverrideCursor()
        QMessageBox.critical(self, "Error", msg)
        SextanteLog.addToLog(SextanteLog.LOG_ERROR, msg)
        keepOpen = SextanteConfig.getSetting(SextanteConfig.KEEP_DIALOG_OPEN)
        if not keepOpen:
            self.dialog.close()
        else:
            self.progressLabel.setText("")
            self.progress.setValue(0)
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)

    @pyqtSlot()
    def cancel(self):
        try:
            self.algEx.finished.disconnect()
            self.algEx.terminate()
            QApplication.restoreOverrideCursor()
            self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setEnabled(False)
        except:
            pass

    def setPercentage(self, i):
        if self.progress.maximum() == 0:
            self.progress.setMaximum(100)
        self.progress.setValue(i)

    def setText(self, text):
        self.progressLabel.setText(text)
