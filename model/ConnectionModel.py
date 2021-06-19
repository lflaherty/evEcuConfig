from model.ObservableField import ObservableField

class ConnectionModel:
    def __init__(self):
        self.serialPorts = ObservableField([])
        self.devices = ObservableField([])

    def notify_all(self):
        self.serialPorts.notifyValueChanged()
        self.devices.notifyValueChanged()
    
    def parse_config(self, configsList):
        devicesList = list(configsList.keys())
        self.devices.set(devicesList)