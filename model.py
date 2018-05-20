from service import SuperService
from service import DefaultHandler


class ModelHandler(DefaultHandler):
    @staticmethod
    def predict(input_data):
        return input_data+' : model predict'

ss = SuperService(ModelHandler)
ss.run('model')
