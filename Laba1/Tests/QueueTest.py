import unittest
from unittest.mock import patch, MagicMock
from Queue import Queue
import random

class TestQueue(unittest.TestCase):

    def test_join_queue_attraction_full(self):
        queue = Queue()
        queue.count_visitors_attract = 15

        queue.join_queue_attraction(10)

        self.assertEqual(queue.count_visitors_attract, 0)

    @patch('builtins.print')
    @patch('time.sleep')
    def test_join_queue_ticket(self, mock_sleep, mock_print):
        queue = Queue()
        queue.count_visitors_ticket = 5  # Assuming there are 5 visitors in the ticket queue

        queue.join_queue_ticket()

        mock_print.assert_any_call("Number of visitors in ticket queue: 5")
        self.assertEqual(mock_sleep.call_count, 5)