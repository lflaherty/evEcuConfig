#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from controller.MainController import MainController
from model.Model import Model


if __name__ == "__main__":
    # Create view
    builder = Gtk.Builder()
    builder.add_from_file("view/view.glade")

    window = builder.get_object("mainWindow")
    window.show_all()

    # Create model & controller
    model = Model()
    controller = MainController(builder, model)
    controller.connectSignals()

    Gtk.main()
