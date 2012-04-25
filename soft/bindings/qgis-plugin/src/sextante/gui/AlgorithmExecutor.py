from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from sextante.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from sextante.core.QGisLayers import QGisLayers
from sextante.core.SextanteUtils import SextanteUtils
from sextante.gui.SextantePostprocessing import SextantePostprocessing

class AlgorithmExecutor:

    @staticmethod
    def runalg(alg, progress):
        '''executes a given algorithm, showing its progress in the progress object passed along.
        Return true if everything went OK, false if the algorithm was canceled or there was
        any problem and could not be completed'''
        try:
            alg.execute(progress)
            return not alg.canceled
        except GeoAlgorithmExecutionException, e :
            QMessageBox.critical(None, "Error", e.msg)
            return False

    @staticmethod
    def runalgIterating(alg,paramToIter,progress):
        #generate all single-feature layers
        settings = QSettings()
        systemEncoding = settings.value( "/UI/encoding", "System" ).toString()
        layerfile = alg.getParameterValue(paramToIter)
        layer = QGisLayers.getObjectFromUri(layerfile, False)
        provider = layer.dataProvider()
        allAttrs = provider.attributeIndexes()
        provider.select( allAttrs )
        feat = QgsFeature()
        filelist = []
        outputs = {}
        while provider.nextFeature(feat):
            output = SextanteUtils.getTempFilename("shp")
            filelist.append(output)
            writer = QgsVectorFileWriter(output, systemEncoding,provider.fields(), provider.geometryType(), provider.crs() )
            writer.addFeature(feat)
            del writer

        #store output values to use them later as basenames for all outputs
        for out in alg.outputs:
            outputs[out.name] = out.value

        #now run all the algorithms
        i = 1
        for f in filelist:
            alg.setParameterValue(paramToIter, f)
            for out in alg.outputs:
                filename = outputs[out.name]
                if filename:
                    filename = filename[:filename.rfind(".")] + "_" + str(i) + filename[filename.rfind("."):]
                out.value = filename
            progress.setText("Executing iteration " + str(i) + "/" + str(len(filelist)) + "...")
            progress.setPercentage((i * 100) / len(filelist))
            if AlgorithmExecutor.runalg(alg, SilentProgress()):
                SextantePostprocessing.handleAlgorithmResults(alg, False)
                i+=1
            else:
                return False;

        return True


class SilentProgress():

    def setText(self, text):
        pass

    def setPercentage(self, i):
        pass
