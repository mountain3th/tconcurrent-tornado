import datetime

import functools
import threading

from concurrent.futures import Future

from tornado.ioloop import IOLoop
from tornado.gen import TimeoutError
import tornado


class ThreadPoolRunner(object):

    class ThreadTask(object):
        @classmethod
        def create_task(cls, fn, *args, **kwargs):
            future = Future()
            def background():
                try:
                    result = fn(*args, **kwargs)
                except Exception as err:
                    future.set_exception(err)
                else:
                    future.set_result(result)
            thread = threading.Thread(target=background)
            thread.daemon = True
            thread.start()

            return future

    @classmethod
    def create_task(cls, fn, *args, **kwargs):
        return ThreadPoolRunner.ThreadTask.create_task(fn, *args, **kwargs)

    @classmethod
    def wraps(cls, seconds=5, error_callback=None, **running_kwargs):
        def decorator(func):
            @functools.wraps(func)
            @tornado.gen.coroutine
            def wrapper(self, *args, **kwargs):
                coroutine_wrapper_func = tornado.gen.coroutine(func)
                result = coroutine_wrapper_func(self, *args, **kwargs)

                callback = running_kwargs.pop('callback', None)
                ioloop = running_kwargs.pop('ioloop', IOLoop.current())

                if callback:
                    result.add_done_callback(callback)
                try:
                    yield tornado.gen.with_timeout(
                        timeout=datetime.timedelta(seconds=seconds),
                        future=result
                    )
                except TimeoutError:
                    pass
                except Exception as err:
                    if error_callback:
                        error_callback(self)
            return wrapper
        return decorator
