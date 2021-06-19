from gi.repository import Gtk
from model.ConnectionModel import ConnectionModel

class ConnectionController:
    def __init__(self, windowBuilder, connectionModel: ConnectionModel):
        # Set up objects
        self.windowBuilder = windowBuilder
        self.connectionModel = connectionModel

        self.connectionModel.devices.onValueChanged(self.onDevicesChanged)
        self.connectionModel.connected.onValueChanged(self.onConnectedChanged)

    # ********************************** Helper methods *************************************

    # ********************************** UI event handlers **********************************
    def onConnectPressed(self, button):
        if not self.connectionModel.connected.get():
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

    def onConnectedChanged(self, connected):
        if connected:
            self.windowBuilder.get_object("connectStatusLabel").set_label('Connected')
            self.windowBuilder.get_object("connectButton").set_sensitive(False)
        else:
            self.windowBuilder.get_object("connectStatusLabel").set_label('Not connected')
            self.windowBuilder.get_object("connectButton").set_sensitive(True)