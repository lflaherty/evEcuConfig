import datetime
from model.ObservableField import ObservableField

class LogModel:
    def __init__(self):
        self.text = ObservableField("")

    def new_log_data(self, data):
        time_str = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        log_entry = '[{}]\t{}\n'.format(time_str, data)
        self.text += log_entry
    
    def notify_all(self):
        self.text.notifyValueChanged()