class ObservableField:
    def __init__(self, initData = None):
        self.notifyValueChangedMethods = []
        self.notifyAppendMethods = []
        self.value = initData

    def onValueChanged(self, method):
        self.notifyValueChangedMethods.append(method)

    def onAppend(self, method):
        self.notifyAppendMethods.append(method)

    def notifyValueChanged(self):
        for notifyMethod in self.notifyValueChangedMethods:
            notifyMethod(self.value)

    def notifyAppend(self, addedData):
        for notifyMethod in self.notifyAppendMethods:
            notifyMethod(self.value, addedData)

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
        self.notifyAppend(other)
        return self    