class ObservableField:
    def __init__(self, initData = None):
        self.notifyMethods = []
        self.value = initData

    def onValueChanged(self, method):
        self.notifyMethods.append(method)
    
    def notifyValueChanged(self):
        for notifyMethod in self.notifyMethods:
            notifyMethod(self.value)

    def set(self, newValue):
        self.value = newValue
        self.notifyValueChanged()
    
    def get(self):
        return self.value
    
    """
    Append data of the target datatype to the interal data.
    """
    def __iadd__(self, other):
        self.value += other
        self.notifyValueChanged()
        return self    