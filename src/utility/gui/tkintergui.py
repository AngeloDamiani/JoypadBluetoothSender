import threading
import time
from tkinter import *
from tkinter.ttk import *

from src.model.bluetoothjoypadcontroller import BluetoothJoypadController
from src.utility.settings.globalsettings import GlobalSettings as GS

from .ui import Ui


class TkinterGui(Frame, Ui):
    def __init__(self, bjc : BluetoothJoypadController):


        # MAIN WINDOW DEFINITION
        root = Tk()
        root.resizable(width=False, height=False)

        # CONTENT FRAME DEFINITION
        content = Frame(root, padding=(10,10,10,10))
        content.grid(column=0, row=0, sticky=(N, S, E, W))


        # BLUETOOTH CONTROLLER ASSIGN
        self.bjc = bjc

        self.root = root
        self.content = content
        self.initUI()

        # SUPPORT VARIABLES
        self.bluetoothname = None
        self.imconnected = False




    def initUI(self):

        # DIMENSION DEFINITION
        ROOTWIDTH = 600
        ROOTHEIGHT = 400
        DEVICEFRAMEWIDTH = int(ROOTWIDTH*(2/3))
        DEVICEFRAMEHEIGHT = ROOTHEIGHT
        STARTFRAMEWIDTH = ROOTWIDTH - DEVICEFRAMEWIDTH
        STARTFRAMEHEIGHT = ROOTHEIGHT

        # WINDOW NAME SET
        self.root.title(GS().getSetting("system_name"))

        # DEVICE LIST FRAME AND FUNCTION FRAME DEFINITION AND SET
        self.device_frame = Frame(self.content, borderwidth=2, width=DEVICEFRAMEWIDTH, height=DEVICEFRAMEHEIGHT)
        self.start_frame = Frame(self.content, borderwidth=2, width=STARTFRAMEWIDTH, height=STARTFRAMEHEIGHT)

        self.device_frame.grid(column = 0, row = 0, columnspan = 2,  sticky=(N, S, E, W))
        self.start_frame.grid(column=3, row=0,  sticky=(N, S, E, W))
        self.device_frame.grid_propagate(False)
        self.start_frame.grid_propagate(False)


        # Let fill the subcontent to device_frame dimensions (in this case: row 1 and column 0)
        self.device_frame.rowconfigure(1,weight = 1)
        self.device_frame.columnconfigure(0,weight = 1)

        # Let fill the subcontent to start_frame dimensions (in this case: row 4 and column 0)
        self.start_frame.columnconfigure(0,weight = 1)
        self.start_frame.rowconfigure(4, weight=1)

        ####################### DEVICE FRAME CONTENT ############################

        device_lable = Label(self.device_frame, text="Select device", padding = (0,0,0,10))
        device_lable.grid(column = 0, row = 0)


        self.device_list = Listbox(self.device_frame, width = 40, height = 2)

        self.device_list.grid(column = 0, row = 1, sticky=(N, S, E, W))

        device_scrollbar = Scrollbar(self.device_frame)
        self.device_list.config(yscrollcommand=device_scrollbar.set)
        device_scrollbar.config(command=self.device_list.yview)
        device_scrollbar.grid(row = 1, column = 2, sticky = (N,S))

        ####################### START FRAME CONTENT #############################

        start_lable = Label(self.start_frame, text="Functions", padding=(0,0,0,10))

        start_lable.grid(column = 0, row = 0)

        self.search_button = Button(self.start_frame, text="Search devices", width = 100, padding=(5,5,5,5))
        self.connect_button = Button(self.start_frame, text="Connect", width = 100, padding=(5,5,5,5))

        self.search_button.grid(column = 0, row = 2, padx=(5,0), pady=5)
        self.connect_button.grid(column = 0, row = 3, padx=(5,0), pady=5)

        self.summary = Text(self.start_frame, height=1000, width=1000)
        self.summary.grid(column = 0, row = 4, sticky=(N, S, E, W), pady = (10,0), padx = (4,0))

        # At start there's no device selected
        self.connect_button.state(["disabled"])
        self.summary.config(state=DISABLED)

        ######################## BUTTON FUNCTION BINDING #########################

        self.search_button.config(command=self.buttonSearchCallBack)
        self.connect_button.config(command=self.buttonConnectCallBack)
        self.device_list.bind('<<ListboxSelect>>', self.deviceSelection)

    def start(self):
        self.root.mainloop()

    def buttonSearchCallBack(self):

        # Start the search on another thread
        waiting_thread = threading.Thread(target=self.devicesSearch, args=())
        waiting_thread.start()

        self.connect_button.config(text = "Connect", command=self.buttonConnectCallBack)

    def buttonConnectCallBack(self):

        # Connect to a target in another thread
        waiting_thread = threading.Thread(target=self.connect, args=())
        waiting_thread.start()

    def buttonDisconnectCallBack(self):
        # Disconnect the service in another thread
        waiting_thread = threading.Thread(target=self.disconnect, args=())
        waiting_thread.start()

    def deviceSelection(self, evt):

        # SAVE IN self.bluetoothname THE CONTENT OF THE SELECTED ITEM IN DEVICE LIST. NEXT
        # IT WILL BE USED FOR FIND AND CONNECT TO THE DEVICE
        if self.device_list.curselection():
            self.bluetoothname = self.device_list.get(self.device_list.curselection()[0])

        # IF SOMETHING IS SELECTED THE BUTTON OF CONNECTION IS ENABLED
        self.connect_button.config(state="normal")

    def devicesSearch(self):

        if self.imconnected:
            self.bjc.disconnect()

        # DISABLING OF BUTTONS ON SEARCH
        self.search_button.config(state="disabled")
        self.connect_button.config(state="disabled")

        # USER FEEDBACK THREAD
        waiting_thread = threading.Thread(target=self._waitingThreadSearch, args=())
        self.waiting = True # WAITING CONDITION OF THE FEEDBACK THREAD
        waiting_thread.start()

        # RETRIEVAL OF NAMES
        name_list = self.bjc.devicesSearch()

        # THE RETRIEVAL IS DONE, FEEDBACK THREAD MUST BE CLOSED
        self.waiting = False

        self.device_list.config(state="normal")

        # DELETE SUMMARY CONTENT AND DEVICE LIST CONTENT (WRITTEN BY FEEDBACK THREAD)
        self._clearDisabledText(self.summary)
        self.device_list.delete(0,END)

        # LIST OF NAMES IS SHOWN
        self.deviceListHandling(name_list)

        # IF THE LIST OF NAME IS EMPTY PRINT A FEEDBACK TO USER IN SUMMARY CONTENT
        if not name_list:
            self._deleteAndWriteOnDisabledText(self.summary,"No device found.")

        # SEARCH BUTTON RE-ENABLED
        self.search_button.config(state="normal")

    def deviceListHandling(self, devices_list):

        # Printing of list of devices into the listbox
        for device in devices_list:
            self.device_list.insert(END, device)

    def connect(self):

        # DISABLING OF BUTTONS ON CONNECTION
        self.search_button.config(state="disabled")
        self.connect_button.config(state="disabled")

        # USER FEEDBACK THREAD
        waiting_thread = threading.Thread(target=self._waitingThreadConnection, args=())
        self.waiting = True  # WAITING CONDITION OF THE FEEDBACK THREAD
        waiting_thread.start()

        res = self.bjc.tryConnection(self.bluetoothname)


        # THE CONNECTION TRIAL IS DONE, FEEDBACK THREAD MUST BE CLOSED
        self.waiting = False

        self.device_list.config(state="normal")

        if res <= 0:
            self.end_wait = self.errorHandling
            self.end_par = res
        else:
            self.end_wait = self.connectionEstablished
            self.end_par = None

        # SEARCH BUTTON RE-ENABLED
        self.search_button.config(state="normal")

    def errorHandling(self, errno):
        string = ""

        self.device_list.config(state="normal")
        self.device_list.delete(0, END)
        # User feedback for failure
        if errno == 0:
            string = "Connection lost or refused."
        elif errno == -1:
            string = "The selected device does not support the service written in configuration file."
        elif errno == -2:
            string = "Joypad not found."

        self._deleteAndWriteOnDisabledText(self.summary, string)

    def connectionEstablished(self):


        sending_thread = threading.Thread(target=self.bjc.startJoypad, args=())
        sending_thread.start()

        self.imconnected = True

        self._clearDisabledText(self.summary)
        self.device_list.delete(0, END)

        string = "Connection established: \n" \
                 "Name: "+self.bluetoothname+"\n" \
                 "Address: "+self.bjc.getMacByName(self.bluetoothname)
        self._deleteAndWriteOnDisabledText(self.summary, string)
        self.connect2disconnect()

    def connect2disconnect(self):
        self.connect_button.config(state="normal",text="Disconnect", command=self.buttonDisconnectCallBack)

    def disconnect2connect(self):
        self.connect_button.config(state="disabled",text="Connect", command=self.buttonConnectCallBack)
        self._deleteAndWriteOnDisabledText(self.summary, "Disconnected")

    def disconnect(self):
        self.bjc.disconnect()
        self.disconnect2connect()


    def _deleteAndWriteOnDisabledText(self, widget, text):
        widget.config(state='normal')
        widget.delete(1.0, END)
        widget.insert(END, text)
        widget.config(state='disabled')

    def _appendTextDisabledText(self, widget, text):
        widget.config(state='normal')
        widget.insert(END, text)
        widget.config(state='disabled')

    def _clearDisabledText(self,widget):
        widget.config(state='normal')
        widget.delete(1.0, END)
        widget.config(state='disabled')

    def _waitingThreadSearch(self):

        str = "Finding devices "

        self.device_list.delete(0,END)
        self.device_list.insert(END,str+"...")
        self._deleteAndWriteOnDisabledText(self.summary, str)
        self.device_list.config(state="disabled")
        while self.waiting:
            self._appendTextDisabledText(self.summary,".")
            time.sleep(0.5)
        self.device_list.config(state="normal")


    def _waitingThreadConnection(self):

        str = "Connecting "

        self.device_list.delete(0,END)
        self.device_list.insert(END,str+"...")
        self.device_list.config(state="disabled")
        self._deleteAndWriteOnDisabledText(self.summary, str)
        while self.waiting:
            self._appendTextDisabledText(self.summary,".")
            time.sleep(0.5)
        self._end_wait_exe()

    def _end_wait_exe(self):
        if self.end_par:
            self.end_wait(self.end_par)
        else:
            self.end_wait()


