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
        self.updatePaused = False

        # Create mark for scrolling
        text_buffer = self.windowBuilder.get_object('logTextBuffer')
        text_iter_end = text_buffer.get_end_iter()
        self.text_mark_end = text_buffer.create_mark('', text_iter_end, False)

        self.logModel.text.onValueChanged(self.onTextChanged)
        self.logModel.text.onAppend(self.onTextAppend)

    # ********************************** Helper methods *************************************
    def filter_text(self, text_to_filter):
        filtered_text = ''
        if self.logFilter:
            for line in iter(text_to_filter.splitlines()):
                if re.search(self.logFilter, line, re.IGNORECASE):
                    filtered_text += line + '\n'
        else:
            filtered_text = text_to_filter
        return filtered_text

    def reset_text(self):
        filtered_text = self.filter_text(self.logText)
        text_buffer = self.windowBuilder.get_object('logTextBuffer')
        text_buffer.set_text(filtered_text)

    def append_text(self, new_text):
        filtered_text = self.filter_text(new_text)
        text_buffer = self.windowBuilder.get_object('logTextBuffer')
        text_iter_end = text_buffer.get_end_iter()
        text_buffer.insert(text_iter_end, filtered_text)

    def scroll_to_end(self):
        self.windowBuilder.get_object('logText').scroll_to_mark(self.text_mark_end, 0, False, 0, 0)

    # ********************************** UI event handlers **********************************
    def onLogWrapToggled(self, button):
        textBox = self.windowBuilder.get_object("logText")
        wrap = button.get_active()
        if wrap:
            textBox.set_wrap_mode(Gtk.WrapMode.WORD)
        else:
            textBox.set_wrap_mode(Gtk.WrapMode.NONE)

    def onLogPauseToggle(self, button):
        self.updatePaused = button.get_active()
        if self.updatePaused is False:
            # Data will need a full refresh
            self.reset_text()
            self.scroll_to_end()
        
    def onLogFilterUpdated(self, search_entry):
        self.logFilter = search_entry.get_text()
        self.reset_text()


    # ********************************** Model event handlers *******************************
    def onTextChanged(self, text):
        self.logText = text

    def onTextAppend(self, full_text, new_text):
        if not self.updatePaused:
            self.append_text(new_text)
            self.scroll_to_end()