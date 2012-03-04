from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.parameters.ParameterMultipleInput import ParameterMultipleInput
from sextante.parameters.ParameterNumber import ParameterNumber
from sextante.parameters.ParameterRaster import ParameterRaster
from sextante.parameters.ParameterString import ParameterString
from sextante.parameters.ParameterTable import ParameterTable
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterTableField import ParameterTableField
from sextante.parameters.ParameterSelection import ParameterSelection
from sextante.parameters.ParameterRange import ParameterRange
from sextante.parameters.ParameterFixedTable import ParameterFixedTable

class ParameterFactory():

    @staticmethod
    def getFromString(s):
        classes = [ParameterBoolean, ParameterMultipleInput,ParameterNumber,
                   ParameterRaster, ParameterString, ParameterTable, ParameterVector,
                   ParameterTableField, ParameterSelection, ParameterRange, ParameterFixedTable]
        for clazz in classes:
            if s.startswith(clazz().parameterName()):
                return clazz().deserialize(s[len(clazz().parameterName())+1:])