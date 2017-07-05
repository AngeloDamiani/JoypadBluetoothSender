from src.model.ijoypadobserver import *
from src.model.joypadreader import *
from src.utility.net.ibluetooth import IBluetoothModule


class BluetoothJoypadController(IJoypadObserver):
    def __init__(self, bt : IBluetoothModule):
        self.bt = bt
        self.retrieved_addresses = dict()


    def devicesSearch(self):
        # RETRIEVAL OF NAMES
        name_list, name_dict = self.bt.getDevicesByName()
        self.retrieved_addresses = name_dict
        return name_list

    def tryConnection(self, device_name):
        try:
            self.jpr = JoypadReader(self)
        except IndexError:
            return -2
        # CONNECTION TRY
        return self.bt.connect(self.retrieved_addresses.get(device_name))

    def disconnect(self):
        # DISCONNECTION
        self.stopJoypad()
        self.bt.disconnect()

    def getMacByName(self, name):
        # GET MAC BY NAME
        return self.retrieved_addresses.get(name)

    def sendData(self, data):
        # DATA SENDING
        self.bt.sendData(data)

    def startJoypad(self):
        self.jpr.start()

    def stopJoypad(self):
        self.jpr.stopRead()

    def update(self, data):
        self.sendData(data)

    def isJoypadConnected(self):
        return bool(self.jpr)
