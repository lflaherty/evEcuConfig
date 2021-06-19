from gi.repository import Gtk
from controller.HandlerFinder import HandlerFinder
from controller.LogController import LogController

class MainController:
    def __init__(self, windowBuilder, model):
        # Set up objects
        self.windowBuilder = windowBuilder
        self.model = model
        self.logController = LogController(windowBuilder, model.get_log_model())
        
        # Set up event handlers
        handlers = [
            self,
            self.logController
        ]
        self.handlerFinder = HandlerFinder(handlers)

        # First time UI update
        model.notify_all()
    
    def connectSignals(self):
        self.windowBuilder.connect_signals(self.handlerFinder)

    def onDestroy(self, *args):
        Gtk.main_quit()

    def onConnectPressed(self, button):
        print("Connect")