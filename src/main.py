import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utility.gui.tkintergui import *
from src.utility.net.pybluezbluetoothmodule import *
from src.model.bluetoothjoypadcontroller import *

tk = TkinterGui(BluetoothJoypadController(PyBluezBluetoothModule()))
tk.start()