import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sextante.core.AlgorithmProvider import AlgorithmProvider
from sextante.lastools.LasToolsUtils import LasToolsUtils
from sextante.core.SextanteConfig import Setting, SextanteConfig
from sextante.lastools.las2shp import las2shp
from sextante.lastools.las2dem import las2dem
from sextante.lastools.lasboundary import lasboundary
from sextante.lastools.las2iso import las2iso
from sextante.lastools.lasgrid import lasgrid
from sextante.lastools.lasground import lasground
from sextante.lastools.lasinfo import lasinfo


class LasToolsAlgorithmProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)
        self.algsList = [las2shp(), lasboundary(), las2dem(), las2iso(), lasgrid(), lasground(), lasinfo()]

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)
        SextanteConfig.addSetting(Setting("LASTools", LasToolsUtils.LASTOOLS_FOLDER, "LASTools folder", LasToolsUtils.LasToolsPath()))
    def getName(self):
        return "LASTools"

    def getIcon(self):
        return QIcon(os.path.dirname(__file__) + "/../images/tool.png")

    def _loadAlgorithms(self):
        self.algs = self.algsList