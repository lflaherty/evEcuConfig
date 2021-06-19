from gi.repository import Gtk
from controller.HandlerFinder import HandlerFinder

class MainController:
    def __init__(self):
        handlers = [
            self,
        ]
        self.handlerFinder = HandlerFinder(handlers)
    
    def connectSignals(self, builder):
        builder.connect_signals(self.handlerFinder)

    def onDestroy(self, *args):
        Gtk.main_quit()

    def onConnectPressed(self, button):
        print("Connect")