from ..metaclasses.metasingleton import *
import bluetooth

from ..settings.globalsettings import *

class PyBluezBluetoothModule(metaclass=MetaSingleton):
    def __init__(self):
        pass

    def getDevices(self):
        # DEVICE MAC RETRIEVAL

        ret = []
        try:
            ret = bluetooth.discover_devices()
        except bluetooth.BluetoothError:
            ret = []
        finally:
            return ret

    def getDevicesByName(self):
        # DEVICE NAME RETRIEVAL

        nearby_devices = self.getDevices()
        name_devices = []
        name_dict = dict()
        if nearby_devices:
            for bdaddr in nearby_devices:
                name = bluetooth.lookup_name(bdaddr)
                if name:
                    name_dict[name] = bdaddr
                    name_devices.append(name)

        return name_devices, name_dict

    def connect(self, address):

        ##CONNECTION ATTEMPT TO ADDRESS

        bd_addr = address


        service_name = GlobalSettings().getSetting("bluetooth").get("service_name")

        ## IF WE NEED A SPECIFIC SERVICE WE READ FROM CONFIG FILE
        if service_name != "":
            try:
                services = bluetooth.find_service(address = address)
                target = None

                for service in services:
                    print(service)
                    if service.get('name') == service_name:
                        target = service
                        break

                port = target.get('port')
                proto = target.get('protocol')
                if proto == "L2CAP":
                    proto = bluetooth.L2CAP
                else:
                    proto = bluetooth.RFCOMM
            except Exception:
                return -1

        ## OTHERWISE WE TRY THE CONNECTION ON PORT 1 (I.E. HC-05/HC-06 MODULES) WITH RFCOMM
        else:
            proto = bluetooth.RFCOMM
            port = 1

        self.sock = bluetooth.BluetoothSocket(proto)
        try:
            self.sock.connect((bd_addr, port))
            return 1
        except bluetooth.BluetoothError:
            return 0


    def sendData(self, data):
        ba = self._intToByteArray(data)
        for i in ba:
            #print(i)
            self.sock.send(bytes([i]))
        #print()

    def disconnect(self):
        self.sock.close()

    def _intToByteArray(self, toBeConverted):

        result = []

        intBytes = 9

        mask = 0xFF

        for i in range(0, intBytes):
            result.insert(0, toBeConverted & mask)
            toBeConverted >>= 8

        return result