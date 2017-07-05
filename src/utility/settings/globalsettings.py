import json, os

from ..metaclasses import MetaSingleton


class GlobalSettings(metaclass=MetaSingleton):

    # ABT_SPP_Service_1

    def __init__(self):
        self._settingpath = os.path.dirname(os.path.abspath(__file__))+"/programsettings.json"
        self._settings = dict()
        self._setup()

    def getSetting(self, setting: str):
        """
        Retrieve the speciefied global setting
        :param setting: Setting to be got
        """
        return self._settings.get(setting)

    def _setup(self):
        with open(self._settingpath) as settings_file:
            self._settings = {**self._settings, **json.load(settings_file)}