from service import SuperService
from service import DefaultHandler
import tornado.escape


class ModelHandler(DefaultHandler):
    def predict(self, input_data):
        data = tornado.escape.json_decode(self.request.body)
        res = 'input_data+ : model predict\n'
        a = int(data['a'])
        b = int(data['b'])
        return res+'summa = '+str(a+b)

ss = SuperService(ModelHandler)
ss.run('model')
