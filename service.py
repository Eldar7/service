import tornado.ioloop
import tornado.web


class DefaultHandler(tornado.web.RequestHandler):
    def initialize(self, msg):
        self.msg = msg

    def get(self):
        self.write("GET: Hello, world " + self.msg)

    def post(self):
        self.write("POST: " + self.predict(self.msg))

    @staticmethod
    def predict(input_data):
        return input_data+' : default predict'


class SuperService():
    def __init__(self, handler):
        self.handler = handler

    def make_app(self, msg):
        return tornado.web.Application([
            (r"/", self.handler, dict(msg=msg)),
        ])

    def run(self, msg):
        app = self.make_app(msg)
        app.listen(1111)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    ss = SuperService(DefaultHandler)
    ss.run('super')
