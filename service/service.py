import tornado.ioloop
import tornado.web
import tornado.escape


class DefaultHandler(tornado.web.RequestHandler):
    def initialize(self, input_data, predict):
        self.input_data = input_data
        self.predict = predict

    def get(self):
        self.write("Hello, world from : " + self.input_data)

    def post(self):
        # https://stackoverflow.com/a/28140966/2436590
        data = tornado.escape.json_decode(self.request.body)
        self.write(self.predict(data))


class SuperService:
    def __init__(self, predict, port, n_proc):
        self.predict = predict
        self.port = port
        self.n_proc = n_proc

    def make_service(self, input_data):
        return tornado.web.Application([
            (r"/", DefaultHandler, dict(input_data=input_data, predict=self.predict)),
        ])

    def start_service(self, service):
        server = tornado.httpserver.HTTPServer(service)
        server.bind(self.port)
        server.start(self.n_proc)
        # service.listen(self.port)
        tornado.ioloop.IOLoop.current().start()

    def run(self, input_data):
        service = self.make_service(input_data)
        self.start_service(service)


def default_predict(data):
    return 'default predict ' + str(data)


if __name__ == "__main__":
    ss = SuperService(default_predict)
    ss.run('default')
