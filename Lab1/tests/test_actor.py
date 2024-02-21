import unittest
from Actor import Actor


class ActorTestCase(unittest.TestCase):

    def test_getters_actor(self):
        actor = Actor("Bob")
        self.assertEqual(actor.get_name(), "Bob")
        self.assertEqual(actor.get_age(), 15)
