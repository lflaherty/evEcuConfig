from model.LogModel import LogModel

class Model:
    def __init__(self):
        self.logModel = LogModel()

        # startup worker
        self.serial_service()
    
    def get_log_model(self):
        return self.logModel
    
    def notify_all(self):
        self.logModel.notify_all()

    def serial_service(self):
        # TODO set up serial message reading here
        # TODO decode serial data
        self.logModel.new_log_data('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam tincidunt finibus ullamcorper. Curabitur nisi ante, aliquet sit amet convallis et, lacinia a ipsum. Interdum et malesuada fames ac ante ipsum primis in faucibus. Quisque a scelerisque lacus, sit amet elementum nunc. Donec id efficitur ex, ut gravida est. Pellentesque ex mauris, dapibus mollis aliquet ut, tempor eu ipsum. Sed auctor odio ut est semper tincidunt. Etiam sollicitudin luctus sem, et maximus risus condimentum ut. Quisque pulvinar luctus lectus, eget rutrum ante semper sed. Ut sit amet laoreet dui, eu efficitur nibh. Nullam eget ipsum pretium, volutpat mi at, vehicula tortor. Etiam maximus eros sit amet facilisis vestibulum.')
        self.logModel.new_log_data('Phasellus semper ultrices faucibus. Donec vel ex varius, facilisis justo eu, dignissim sem. In ac accumsan nisl. In sit amet tempus erat. Sed faucibus urna quis tellus tristique, at rhoncus enim hendrerit. Donec non posuere augue. Ut pharetra nunc sed purus viverra eleifend. Etiam at tincidunt libero. Vestibulum in bibendum dolor. Nunc vitae elementum quam. Praesent lacinia libero a congue placerat. Praesent auctor lacus id sollicitudin tincidunt. Sed tempus leo id felis pharetra suscipit. Vivamus tincidunt quis massa ac scelerisque. Aenean sed erat commodo ante faucibus maximus. Curabitur velit erat, placerat eget faucibus vitae, scelerisque ut mauris.')