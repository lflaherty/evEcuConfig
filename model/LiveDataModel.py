from model.ObservableField import ObservableField

class LiveDataModel:
    def __init__(self):
        self.liveFields = ObservableField({})
        self.fieldValues = ObservableField({})

    def parse_config(self, config):
        dataFields = {field['ID']: field for field in config['LiveDataFields']}
        self.liveFields.set(dataFields)
    
    def update_field(self, field_id, value):
        if field_id in self.liveFields.get():
            if self.liveFields.get()[field_id]['Convert']:
                offset = self.liveFields.get()[field_id]['ConversionBias']
                scale = self.liveFields.get()[field_id]['ConversionScale']
                realValue = scale * value + offset
            else:
                realValue = value

            self.fieldValues.get()[field_id] = str(realValue)
            self.fieldValues.notifyValueChanged()
    
    def get_field_value(self, field_id):
        if field_id in self.fieldValues.get():
            return self.fieldValues.get()[field_id] 
        else:
            return None