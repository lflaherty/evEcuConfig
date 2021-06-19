from typing import NewType
import re
from gi.repository import Gtk

from model.LogModel import LogModel

class LogController:
    def __init__(self, windowBuilder, logModel: LogModel):
        self.windowBuilder = windowBuilder
        self.logModel = logModel

        self.logText = ''
        self.logFilter = ''

        self.logModel.text.onValueChanged(self.onTextChanged)

    # ********************************** Helper methods *************************************
    def update_visible_text(self):
        filtered_text = ''
        if self.logFilter:
            for line in iter(self.logText.splitlines()):
                if re.search(self.logFilter, line, re.IGNORECASE):
                    filtered_text += line + '\n'
        else:
            filtered_text = self.logText
        self.windowBuilder.get_object("logTextBuffer").set_text(filtered_text)

    # ********************************** UI event handlers **********************************
    def onLogWrapToggled(self, button):
        textBox = self.windowBuilder.get_object("logText")
        wrap = button.get_active()
        if wrap:
            textBox.set_wrap_mode(Gtk.WrapMode.WORD)
        else:
            textBox.set_wrap_mode(Gtk.WrapMode.NONE)
        
    def onLogFilterUpdated(self, search_entry):
        self.logFilter = search_entry.get_text()
        self.update_visible_text()


    # ********************************** Model event handlers *******************************
    def onTextChanged(self, text):
        self.logText = text
        self.update_visible_text()