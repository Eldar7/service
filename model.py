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
        res = self.message
        a = int(data['a'])
        b = int(data['b'])
        return res + 'sum = ' + str(a + b)


if __name__ == "__main__":
    #https://github.com/tornadoweb/tornado/issues/1669
    #on Windows support only n_proc=1
    ss = SuperService(Predictor, port=1111, n_proc=1)
    ss.run('model')
