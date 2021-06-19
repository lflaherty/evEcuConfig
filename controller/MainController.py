from gi.repository import Gtk
from model.Model import Model
from controller.HandlerFinder import HandlerFinder
from controller.ConnectionController import ConnectionController
from controller.LogController import LogController

class MainController:
    def __init__(self, windowBuilder, model: Model):
        # Set up objects
        self.windowBuilder = windowBuilder
        self.model = model
        self.connectionController = ConnectionController(windowBuilder, model.get_connection_model())
        self.logController = LogController(windowBuilder, model.get_log_model())
        
        # Set up event handlers
        handlers = [
            self,
            self.connectionController,
            self.logController,
        ]
        self.handlerFinder = HandlerFinder(handlers)

        # First time UI update
        model.notify_all()

    # ********************************** Helper methods *************************************
    def connectSignals(self):
        self.windowBuilder.connect_signals(self.handlerFinder)
        self.model.get_connection_model().connected.onValueChanged(self.onDeviceConnected)
    
    def loadConfig(self):
        pass

    # ********************************** UI event handlers **********************************
    def onDestroy(self, *args):
        Gtk.main_quit()

    # ********************************** Model event handlers *******************************
    def onDeviceConnected(self, connected):
        # Trigger the config to load
        self.loadConfig()