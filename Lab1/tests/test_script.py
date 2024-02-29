import unittest
from Script import Script


class ScriptTestCase(unittest.TestCase):

    def test_getters_script(self):
        script = Script("first", "horror", 5, "hello", 0)
        self.assertEqual(script.get_name(), "first")
        self.assertEqual(script.get_film_type(), "horror")
        script.set_actors_number(3)
        self.assertEqual(script.get_actors_number(), 3)
        self.assertEqual(script.get_plot(), "hello")
        self.assertEqual(script.get_experience_director(), 0)
