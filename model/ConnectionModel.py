from model.ObservableField import ObservableField

class ConnectionModel:
    def __init__(self):
        self.serialPorts = ObservableField([])
        self.devices = ObservableField([])
        self.connected = ObservableField(False)
        self.connectedDevice = None

    def notify_all(self):
        self.serialPorts.notifyValueChanged()
        self.devices.notifyValueChanged()
    
    def parse_config(self, configsList):
        devicesList = list(configsList.keys())
        self.devices.set(devicesList)
    
    def get_connected_device(self):
        return self.connectedDeviceName
    
    def perform_connect(self, deviceIndex, serialIndex):
        print('Connecting to', self.devices.get()[deviceIndex], 'at', serialIndex)

        # Make the rest of the config load in other models
        self.connectedDeviceName = self.devices.get()[deviceIndex]
        self.connected.set(True)