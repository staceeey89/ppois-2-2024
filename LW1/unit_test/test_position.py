from Position import Position

import unittest
class TestPosition(unittest.TestCase):

    def test_enum_values(self):
        self.assertEqual(Position.DEVELOPER.value, "Developer")
        self.assertEqual(Position.TESTER.value, "Tester")
        self.assertEqual(Position.QA.value, "QA")
        self.assertEqual(Position.DESIGNER.value, "Designer")
        self.assertEqual(Position.DIRECTOR.value, "Director")
        self.assertEqual(Position.HR.value, "HR")
        self.assertEqual(Position.MANAGER.value, "Manager")
        self.assertEqual(Position.ANALYTICS.value, "Analytics")

    def test_enum_membership(self):
        self.assertTrue(Position.DEVELOPER in Position)
        self.assertTrue(Position.TESTER in Position)
        self.assertTrue(Position.QA in Position)
        self.assertTrue(Position.DESIGNER in Position)
        self.assertTrue(Position.DIRECTOR in Position)
        self.assertTrue(Position.HR in Position)
        self.assertTrue(Position.MANAGER in Position)
        self.assertTrue(Position.ANALYTICS in Position)


if __name__ == "__main__":
    unittest.main()
