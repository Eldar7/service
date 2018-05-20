import tornado.ioloop
import tornado.web
import tornado.escape


class DefaultHandler(tornado.web.RequestHandler):
    def initialize(self, input_data):
        self.input_data = input_data

    def get(self):
        self.write("GET: Hello, world " + self.input_data)

    def post(self):
        self.write("POST: " + self.predict(self.input_data))

    def predict(self, input_data):
        # https://stackoverflow.com/a/28140966/2436590
        data = tornado.escape.json_decode(self.request.body)
        return input_data + ' : default predict \ndata = ' + str(data)


class SuperService():
    def __init__(self, handler):
        self.handler = handler

    def make_app(self, input_data):
        return tornado.web.Application([
            (r"/", self.handler, dict(input_data=input_data)),
        ])

    def run(self, input_data):
        app = self.make_app(input_data)
        app.listen(1111)
        tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    ss = SuperService(DefaultHandler)
    ss.run('super')
