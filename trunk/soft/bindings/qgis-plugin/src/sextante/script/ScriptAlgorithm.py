from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.parameters.ParameterRaster import ParameterRaster
from sextante.parameters.ParameterTable import ParameterTable
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterMultipleInput import ParameterMultipleInput
from sextante.script.WrongScriptException import WrongScriptException
from sextante.outputs.OutputTable import OutputTable
from sextante.outputs.OutputVector import OutputVector
from sextante.outputs.OutputRaster import OutputRaster
from sextante.parameters.ParameterString import ParameterString
from sextante.parameters.ParameterNumber import ParameterNumber
from sextante.parameters.ParameterBoolean import ParameterBoolean
import os
from sextante.parameters.ParameterSelection import ParameterSelection
from PyQt4 import QtGui
from sextante.parameters.ParameterTableField import ParameterTableField

class ScriptAlgorithm(GeoAlgorithm):

    def __init__(self, descriptionfile):
        GeoAlgorithm.__init__(self)
        self.descriptionFile = descriptionfile
        self.defineCharacteristicsFromFile()


    def getIcon(self):
        return QtGui.QIcon(os.path.dirname(__file__) + "/../images/script.png")


    def defineCharacteristicsFromFile(self):
        self.script=""
        self.silentOutputs = []
        filename = os.path.basename(self.descriptionFile)
        self.name = filename[:filename.rfind(".")].replace("_", " ")
        self.group = "User scripts"
        lines = open(self.descriptionFile)
        line = lines.readline()
        while line != "":
            if line.startswith("##"):
                self.processParameterLine(line.strip("\n"))
            self.script += line
            line = lines.readline()
        lines.close()


    def processParameterLine(self,line):

        param = None
        out = None
        line = line.replace("#", "");
        tokens = line.split("=");
        if tokens[1].lower().strip() == "group":
            self.group = tokens[0]
        if tokens[1].lower().strip() == "raster":
            param = ParameterRaster(tokens[0], tokens[0], False)
        elif tokens[1].lower().strip() == "vector":
            param = ParameterVector(tokens[0], tokens[0],ParameterVector.VECTOR_TYPE_ANY)
        elif tokens[1].lower().strip() == "table":
            param = ParameterTable(tokens[0], tokens[0], False)
        elif tokens[1].lower().strip() == "multiple raster":
            param = ParameterMultipleInput(tokens[0], tokens[0], ParameterMultipleInput.TYPE_RASTER)
            param.optional = False
        elif tokens[1].lower().strip() == "multiple vector":
            param = ParameterMultipleInput(tokens[0], tokens[0], ParameterMultipleInput.TYPE_VECTOR_ANY)
            param.optional = False
        elif tokens[1].lower().strip().startswith("selection"):
            options = tokens[1].strip()[len("selection"):].split(";")
            param = ParameterSelection(tokens[0],  tokens[0], options);
        elif tokens[1].lower().strip() == "boolean":
            default = tokens[1].strip()[len("boolean")+1:]
            param = ParameterBoolean(tokens[0],  tokens[0], default)
        elif tokens[    1].lower().strip().startswith("number"):
            default = tokens[1].strip()[len("number")+1:]
            param = ParameterNumber(tokens[0],  tokens[0], default=default)
        elif tokens[1].lower().strip().startswith("field"):
            field = tokens[1].strip()[len("field")+1:]
            found = False
            for p in self.parameters:
                if p.name == field:
                    found = True
                    break
            if found:
                param = ParameterTableField(tokens[0],  tokens[0], field)
        elif tokens[1].lower().strip().startswith("string"):
            default = tokens[1].strip()[len("string")+1:]
            param = ParameterString(tokens[0],  tokens[0], default)
        elif tokens[1].lower().strip().startswith("output raster"):
            out = OutputRaster()
            if tokens[1].strip().endswith("*"):
                self.silentOutputs.append(tokens[0])
        elif tokens[1].lower().strip().startswith("output vector"):
            out = OutputVector()
            if tokens[1].strip().endswith("*"):
                self.silentOutputs.append(tokens[0])
        elif tokens[1].lower().strip().startswith("output table"):
            out = OutputTable()
            if tokens[1].strip().endswith("*"):
                self.silentOutputs.append(tokens[0])

        if param != None:
            self.addParameter(param)
        elif out != None:
            out.name = tokens[0]
            out.description = tokens[0]
            self.addOutput(out)
        else:
            raise WrongScriptException("Could not load script:" + self.descriptionFile + ".\n Problem with line \"" + line + "\"")

    def processAlgorithm(self, progress):

        script = "from sextante.core.Sextante import Sextante\n"
        for param in self.parameters:
            script += param.name + "=" + param.getValueAsCommandLineParameter() + "\n"

        for out in self.outputs:
            script += out.name + "=" + out.getValueAsCommandLineParameter() + "\n"

        script+=self.script
        exec(script)

        for out in self.outputs:
            if out.name in self.silentOutputs:
                out.value = None


