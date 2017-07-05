import abc

class IBluetoothModule(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def getDevices(self):
        pass

    @abc.abstractmethod
    def getDevicesByName(self):
        pass

    @abc.abstractmethod
    def sendData(self, data):
        pass

    @abc.abstractmethod
    def connect(self, address):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass