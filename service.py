import tornado.ioloop
import tornado.web


class SuperService():
    class MainHandler(tornado.web.RequestHandler):
        def initialize(self, msg):
            self.msg = msg

        def get(self):
            self.write("GET: Hello, world " + self.msg)

        def post(self):
            self.write("POST: Hello, world " + self.msg)

    def make_app(self, msg):
        return tornado.web.Application([
            (r"/", self.MainHandler, dict(msg=msg)),
        ])

    def run(self, msg):
        app = self.make_app(msg)
        app.listen(1111)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    ss = SuperService()
    ss.run('super')
