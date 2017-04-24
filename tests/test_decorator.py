import unittest

from concurrent.futures import Future

from src import tconcurrent


class DecoratorTestCase(unittest.TestCase):

    def test_create_task(self):
        """Test create_task exepect a future instance
        """
        def speak():
            print 'i am speaking now'
            return 0

        def finish_callback(result):
            self.assertEqual(result, 0)

        future = tconcurrent.ThreadPoolRunner.create_task(speak)

        self.assertTrue(isinstance(future, Future))

        future.add_done_callback(finish_callback)

    def test_wraps(self):
        """Test wraps concurrently doing multi jobs
        """
        pass

