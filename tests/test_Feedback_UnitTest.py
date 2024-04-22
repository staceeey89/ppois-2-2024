import unittest
from Feedback import Feedback

class TestFeedback(unittest.TestCase):
    
    def setUp(self):
        self.feedback = Feedback()
        
    def test_initialization(self):
        self.assertEqual(self.feedback.getFeedbacks(), [])
        
    def test_add_feedback(self):
        self.feedback.addFeedback("Good service")
        self.assertEqual(self.feedback.getFeedbacks(), ["Good service"])
        
if __name__ == '__main__':
    unittest.main()
