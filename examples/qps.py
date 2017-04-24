import time

from tornado.web import RequestHandler, Application
from tornado import ioloop

from src import tconcurrent
import sys

class TestHandler(RequestHandler):
    __name__ = 'TestHandler'

    @tconcurrent.ThreadPoolRunner.wraps()
    def get(self):
        def time_consuming_job():
            time.sleep(0.5)
        yield tconcurrent.ThreadPoolRunner.create_task(time_consuming_job)
        self.write('test qps')


if __name__ == '__main__':
    application = Application(
        handlers=[(r"/", TestHandler)])
    application.listen(8000, "127.0.0.1")
    ioloop.IOLoop.instance().start()

