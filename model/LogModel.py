from model.ObservableField import ObservableField

class LogModel:
    def __init__(self):
        self.text = ObservableField("")

    def new_log_data(self, data):
        self.text += data + '\n'
    
    def notify_all(self):
        self.text.notifyValueChanged()