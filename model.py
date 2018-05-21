"""
Example of usage.
You can execute 'pip install .' and run model.py from any place.
If you already have this package installed use 'pip install . --upgrade'
"""
from service import SuperService


def predict(data):
    res = 'input_data : model predict\n'
    a = int(data['a'])
    b = int(data['b'])
    return res + 'sum = ' + str(a + b)


if __name__ == "__main__":
    ss = SuperService(predict, 1111)
    ss.run('model')
