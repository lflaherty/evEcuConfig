from gi.repository import Gtk
from model.LiveDataModel import LiveDataModel

class LiveDataController:
    def __init__(self, windowBuilder, liveDataModel: LiveDataModel):
        # Set up objects
        self.windowBuilder = windowBuilder
        self.liveDataModel = liveDataModel

        self.liveDataModel.liveFields.onValueChanged(self.onLiveFieldsChanged)
        self.liveDataModel.fieldValues.onValueChanged(self.onFieldValuesChanged)

    # ********************************** Helper methods *************************************
    def update_field_data(self):
        dataStore = self.windowBuilder.get_object("liveDataListStore")
        for storeEntry in iter(dataStore):
            # Get data for this entry
            fieldId = storeEntry[2]
            currentValue = self.liveDataModel.get_field_value(fieldId)
            storeEntry[1] = currentValue

    # ********************************** UI event handlers **********************************

    # ********************************** Model event handlers *******************************
    def onLiveFieldsChanged(self, liveFields):
        # Update the visible fields
        dataStore = self.windowBuilder.get_object("liveDataListStore")
        dataStore.clear()

        for field in liveFields.values():
            dataStoreEntry = [field["Name"], None, field['ID']]
            dataStore.append(dataStoreEntry)

        # Update data
        self.update_field_data()

    def onFieldValuesChanged(self, fieldValues):
        self.update_field_data()