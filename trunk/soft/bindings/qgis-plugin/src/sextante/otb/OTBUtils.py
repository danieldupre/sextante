import os
import subprocess
from sextante.core.SextanteConfig import SextanteConfig
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteUtils import SextanteUtils

class OTBUtils:

    OTB_FOLDER = "OTB_FOLDER"
    OTB_LIB_FOLDER = "OTB_LIB_FOLDER"

    @staticmethod
    def otbPath():
        folder = SextanteConfig.getSetting(OTBUtils.OTB_FOLDER)
        if folder == None:
            folder =""

        return folder

    @staticmethod
    def otbLibPath():
        folder = SextanteConfig.getSetting(OTBUtils.OTB_LIB_FOLDER)
        if folder == None:
            folder =""

        return folder

    @staticmethod
    def otbDescriptionPath():
        return os.path.join(os.path.dirname(__file__), "description")

    @staticmethod
    def executeOtb(commands, progress):
        loglines = []
        loglines.append("OTB execution console output")
        os.putenv('ITK_AUTOLOAD_PATH', OTBUtils.otbLibPath())
        proc = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True).stdout
        for line in iter(proc.readline, ""):
            if "[*" in line:
                idx = line.find("[*")
                perc = int(line[idx-4:idx-2].strip(" "))
                if perc !=0:
                    progress.setPercentage(perc)
            else:
                loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)



