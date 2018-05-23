"""
Example of usage.
You can execute 'pip install .' and run model.py from any place.
If you already have this package installed use 'pip install . --upgrade'
"""
from service import SuperService


class Predictor:
    def __init__(self, message):
        self.message = message#'default message\t'

    def predict(self, data):
        res = self.message + '\t'
        a = int(data['a'])
        b = int(data['b'])
        return res + 'a = ' + str(a) + '; b = ' + str(b)


class PredictorMul(Predictor):
    def predict(self, data):
        res = self.message + '\t'
        a = int(data['a'])
        b = int(data['b'])
        return res + 'mul = ' + str(a * b)


class PredictorSum(Predictor):
    def predict(self, data):
        res = self.message + '\t'
        a = int(data['a'])
        b = int(data['b'])
        return res + 'sum = ' + str(a + b)


if __name__ == "__main__":
    #https://github.com/tornadoweb/tornado/issues/1669
    #on Windows support only n_proc=1
    url_predictor_dict = {'/': Predictor, '/sum':PredictorSum, '/mul':PredictorMul}
    ss = SuperService(url_predictor_dict, port=1111, n_proc=1)
    ss.run('model')
