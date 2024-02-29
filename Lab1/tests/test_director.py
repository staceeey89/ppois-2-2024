import unittest
from Director import Director
from Script import Script


class DirectorTestCase(unittest.TestCase):

    def test_change_experience(self):
        director = Director("Billy")
        script = Script("one", "horror", 5, "mes", 0)

        result = director.change_experience(0, script)
        self.assertTrue(result)
        self.assertEqual(director.get_experience(), 0)

        result = director.change_experience(1, script)
        self.assertTrue(result)
        self.assertEqual(director.get_experience(), 1)

        result = director.change_experience(2, script)
        self.assertTrue(result)
        self.assertEqual(director.get_experience(), 2)

        result = director.change_experience(3, script)
        self.assertFalse(result)

        result = director.get_name()
        self.assertEqual(result, "Billy")
