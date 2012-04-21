from sextante.core.SextanteUtils import SextanteUtils

class Output(object):

    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.value = None
        # a hidden output will not be shown to the user, who will not be able to select where to store it
        # Use this to generate outputs that are modified version of inputs (like a selection in a vector layer)
        # In the case of layers, hidden outputs are not loaded into QGIS after the algorithm is executed.
        # Other outputs not representing layers or tables should always be hidden.
        self.hidden = False

    def __str__(self):
        return self.name + " <" + self.__module__.split(".")[-1] +">"

    def getValueAsCommandLineParameter(self):
        if self.value == None:
            return str(None)
        else:
            if not SextanteUtils.isWindows():
                return "\"" + str(self.value) + "\""
            else:
                return "\"" + str(self.value).replace("\\", "\\\\") + "\""

    def serialize(self):
        return self.__module__.split(".")[-1] + "|" + self.name + "|" + self.description

    def setValue(self, value):
        try:
            if value != None:
                value = value.strip()
            self.value = value
            return True
        except:
            return False

    def outputTypeName(self):
        return self.__module__.split(".")[-1]