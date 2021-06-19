#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from controller.MainController import MainController


if __name__ == "__main__":
    controller = MainController()

    # Create view
    builder = Gtk.Builder()
    builder.add_from_file("view/view.glade")
    controller.connectSignals(builder)

    window = builder.get_object("mainWindow")
    window.show_all()

    Gtk.main()
