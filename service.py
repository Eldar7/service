import tornado.ioloop
import tornado.web
import tornado.escape


class DefaultHandler(tornado.web.RequestHandler):
    def initialize(self, input_data, predict):
        self.input_data = input_data
        self.predict = predict

    def get(self):
        self.write("GET: Hello, world from : " + self.input_data)

    def post(self):
        # https://stackoverflow.com/a/28140966/2436590
        data = tornado.escape.json_decode(self.request.body)
        self.write("POST: " + self.predict(data))


class SuperService:
    def __init__(self, predict):
        self.predict = predict

    def make_app(self, input_data):
        return tornado.web.Application([
            (r"/", DefaultHandler, dict(input_data=input_data, predict=self.predict)),
        ])

    def run(self, input_data):
        app = self.make_app(input_data)
        app.listen(1111)
        tornado.ioloop.IOLoop.current().start()


def default_predict(data):
    return 'default predict ' + str(data)


if __name__ == "__main__":
    ss = SuperService(default_predict)
    ss.run('default')
