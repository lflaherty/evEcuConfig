from gi.repository import Gtk

class MainController:
    def __init__(self):
        pass

    def onDestroy(self, *args):
        Gtk.main_quit()

    def onConnectPressed(self, button):
        print("Connect")