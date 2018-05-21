from service import SuperService


def predict(data):
    res = 'input_data : model predict\n'
    a = int(data['a'])
    b = int(data['b'])
    return res + 'sum = ' + str(a + b)


ss = SuperService(predict)
ss.run('model')
