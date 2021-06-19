from gi.repository import Gtk
from model.ConnectionModel import ConnectionModel

class ConnectionController:
    def __init__(self, windowBuilder, connectionModel: ConnectionModel):
        # Set up objects
        self.windowBuilder = windowBuilder
        self.connectionModel = connectionModel

        self.connectionModel.devices.onValueChanged(self.onDevicesChanged)

    # ********************************** Helper methods *************************************

    # ********************************** UI event handlers **********************************
    def onConnectPressed(self, button):
        # Make the model open the connection
        selectedDevice = self.windowBuilder.get_object("deviceListComboBox").get_active()
        selectedSerial = self.windowBuilder.get_object("serialPortComboBox").get_active()
        self.connectionModel.perform_connect(selectedDevice, selectedSerial)

        # Enable rest of UI
        self.windowBuilder.get_object("mainNotebook").set_sensitive(True)

    # ********************************** Model event handlers *******************************
    def onDevicesChanged(self, devices):
        dataStore = self.windowBuilder.get_object("devicesListStore")
        dataStore.clear()
        for device in devices:
            dataStore.append([device])
        
        self.windowBuilder.get_object("deviceListComboBox").set_active(0)