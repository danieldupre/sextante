from sextante.core.SextanteUtils import SextanteUtils
import os.path

class SextanteConfig():

    OUTPUT_FOLDER = "OUTPUT_FOLDER"
    RASTER_STYLE = "RASTER_STYLE"
    VECTOR_POINT_STYLE = "VECTOR_POINT_STYLE"
    VECTOR_LINE_STYLE = "VECTOR_LINE_STYLE"
    VECTOR_POLYGON_STYLE = "VECTOR_POLYGON_STYLE"
    SHOW_RECENT_ALGORITHMS = "SHOW_RECENT_ALGORITHMS"
    USE_SELECTED = "USE_SELECTED"
    USE_FILENAME_AS_LAYER_NAME = "USE_FILENAME_AS_LAYER_NAME"

    settings = {}

    @staticmethod
    def initialize():
        SextanteConfig.addSetting(Setting("General", SextanteConfig.USE_SELECTED, "Use only selected features in external application", True))
        SextanteConfig.addSetting(Setting("General", SextanteConfig.USE_FILENAME_AS_LAYER_NAME, "Use filename as layer name", True))
        SextanteConfig.addSetting(Setting("General", SextanteConfig.SHOW_RECENT_ALGORITHMS, "Show recently executed algorithms", True))
        SextanteConfig.addSetting(Setting("General", SextanteConfig.OUTPUT_FOLDER,
                                           "Output folder", SextanteUtils.tempFolder()))
        SextanteConfig.addSetting(Setting("General", SextanteConfig.RASTER_STYLE,"Style for raster layers",""))
        SextanteConfig.addSetting(Setting("General", SextanteConfig.VECTOR_POINT_STYLE,"Style for point layers",""))
        SextanteConfig.addSetting(Setting("General", SextanteConfig.VECTOR_LINE_STYLE,"Style for line layers",""))
        SextanteConfig.addSetting(Setting("General", SextanteConfig.VECTOR_POLYGON_STYLE,"Style for polygon layers",""))

    @staticmethod
    def addSetting(setting):
        SextanteConfig.settings[setting.name] = setting

    @staticmethod
    def removeSetting(name):
        del SextanteConfig.settings[name]

    @staticmethod
    def getSettings():
        settings={}
        for setting in SextanteConfig.settings.values():
            if not setting.group in settings:
                group = []
                settings[setting.group] = group
            else:
                group = settings[setting.group]
            group.append(setting)
        return settings

    @staticmethod
    def configFile():
        return os.path.join(SextanteUtils.userFolder(), "sextante_qgis.conf")

    @staticmethod
    def loadSettings():
        if not os.path.isfile(SextanteConfig.configFile()):
            return
        lines = open(SextanteConfig.configFile())
        line = lines.readline().strip("\n")
        while line != "":
            tokens = line.split("=")
            if tokens[0] in SextanteConfig.settings.keys():
                setting = SextanteConfig.settings[tokens[0]]
                if isinstance(setting.value, bool):
                    setting.value = (tokens[1].strip() == str(True))
                else:
                    setting.value = tokens[1]
                SextanteConfig.addSetting(setting)
            line = lines.readline().strip("\n")
        lines.close()

    @staticmethod
    def saveSettings():
        fout = open(SextanteConfig.configFile(), "w")
        for setting in SextanteConfig.settings.values():
            fout.write(str(setting) + "\n")
        fout.close()

    @staticmethod
    def getSetting(name):
        if name in SextanteConfig.settings.keys():
            return SextanteConfig.settings[name].value
        else:
            return None

    @staticmethod
    def setSettingValue(name, value):
        if name in SextanteConfig.settings.keys():
            SextanteConfig.settings[name].value = value
            SextanteConfig.saveSettings()


class Setting():
    '''A simple config parameter that will appear on the SEXTANTE config dialog'''
    def __init__(self, group, name, description, default):
        self.group=group
        self.name = name
        self.description = description
        self.default = default
        self.value = default

    def __str__(self):
        return self.name + "=" + str(self.value)