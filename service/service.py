import tornado.ioloop
import tornado.web
import tornado.escape

import sys
import os
import logging
import logging.config

PATH_TO_DIR = os.path.abspath(os.path.dirname(__file__))
LOGGING_CONF_PATH = PATH_TO_DIR + '\logging.conf'

logger = logging.getLogger(__name__)


def logging_conf_updater(logging_conf_path=LOGGING_CONF_PATH, ptd=PATH_TO_DIR):
    print(logging_conf_path)
    try:
        logging.config.fileConfig(os.path.join(ptd, logging_conf_path), disable_existing_loggers=False)
    except:
        try:
            logging.config.fileConfig(os.path.join(ptd, sys.prefix+'/service/logging.conf'), disable_existing_loggers=False)
        except Exception as e:
            raise e


class DefaultHandler(tornado.web.RequestHandler):
    def initialize(self, input_data, predict):
        self.input_data = input_data
        self.predict = predict

    def get(self):
        logger.info('Received GET query on: ' + self.request.uri)
        try:
            rec = "Hello, world from : " + self.input_data
            self.write(rec)
            logger.info('Get result: ' + str(rec))
        except Exception as e:
            logger.exception('Can not process GET query with error: ' + str(e))
            raise e
        else:
            logger.info('GET query processed')

    def post(self):
        logger.info('Received POST query on: ' + self.request.uri)
        logger.info('Received post data: ' + str(self.request.body))  # WAS '.debug'

        # https://stackoverflow.com/a/28140966/2436590
        try:
            data = tornado.escape.json_decode(self.request.body)
            logger.info(str(data))  # Can be safely deleted
        except Exception as e:
            logger.exception('Can not parse POST data with error: ' + str(e))
            raise e

        try:
            rec = self.predict(data)
            self.write(rec)
            logger.info('Predict: ' + str(rec))
        except Exception as e:
            logger.exception('Can not make predict with error: ' + str(e))
            raise e
        else:
            logger.info('Prediction successfully done')


class SuperService:
    def __init__(self, url_predictor_dict, port=1111, n_proc=1):
        logging_conf_updater()
        self.port = port
        self.n_proc = n_proc
        try:
            self.url_predictor_dict = dict()
            for url in url_predictor_dict:
                self.url_predictor_dict[url] = url_predictor_dict[url](url)
            logger.info('Predictor(s) '+str(url_predictor_dict)+' successfully created')#TODO почему-то из этого места логи не выводятся, разобраться
        except Exception as e:
            logger.exception('Can create Predictor with error: ' + str(e))
            raise e

    def make_service(self, input_data):
        logger.info('Start configuring service')
        service_settings = [
            (url, DefaultHandler, dict(input_data=input_data, predict=self.url_predictor_dict[url].predict))
            for url in self.url_predictor_dict
        ]
        logger.info(service_settings)

        try:
            service = tornado.web.Application(service_settings)
        except Exception as e:
            logger.exception('Can not configure service with error: ' + str(e))
            raise e

        logger.info('Service successfully configured')
        return service

    def start_service(self, service):
        logger.info('Start service ' + str(service))
        logger.debug('Service port: ' + str(self.port))

        try:
            # service.listen(self.port)
            server = tornado.httpserver.HTTPServer(service)
            server.bind(self.port)
            server.start(self.n_proc)
        except Exception as e:
            logger.exception('Can not start service with error: ' + str(e))
            raise e

        logger.info('Service successfully started at port: ' + str(self.port))
        tornado.ioloop.IOLoop.current().start()

    def run(self, input_data):
        service = self.make_service(input_data)
        self.start_service(service)


class Predictor:
    def __init__(self, message):
        self.message = message
    def predict(self, data):
        return self.message + str(data)


if __name__ == "__main__":
    ss = SuperService({'/':Predictor})
    ss.run('default')
