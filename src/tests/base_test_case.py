import logging
import unittest
from controller.app import app
from localstack_utils.localstack import startup_localstack, stop_localstack
from infrastructure.aws_sqs import create_sqs_queue


class BaseTestCase(unittest.TestCase):
    test_file = 'test.csv'

    def setUp(self):
        logging.debug("setUp")
        startup_localstack()
        create_sqs_queue("process")
        self.app = app
        self.client = self.app.test_client()

    def tearDown(self):
        stop_localstack()
        logging.debug("tearDown")


