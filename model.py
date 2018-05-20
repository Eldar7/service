from service import SuperService
from service import DefaultHandler
import tornado.escape


class ModelHandler(DefaultHandler):
    def predict(self, input_data):
        data = tornado.escape.json_decode(self.request.body)
        return input_data+' : model predict\ndata = '+str(data)

ss = SuperService(ModelHandler)
ss.run('model')
