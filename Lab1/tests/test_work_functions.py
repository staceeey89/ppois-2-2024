import unittest
from unittest.mock import patch
from Camera import Camera
from Montage import Montage
from PostProduction import PostProduction
import WorkFunctions as wf


class WorkFunctionsTestCase(unittest.TestCase):

    @patch('builtins.input', side_effect=['first', 's', '-1', '1', 's', '1', '1', '1', '0'])
    def test_create_studio(self, mock_input):
        studio = wf.create_studio()
        self.assertEqual(studio.get_name(), "first")
        self.assertEqual(studio.get_person_number(), 1)
        self.assertEqual(len(studio.get_list_old_persons()), 0)
        self.assertEqual(len(studio.get_list_young_persons()), 0)

    @patch('builtins.input', side_effect=['horror'])
    def test_create_filmset(self, mock_input):
        film_set = wf.create_filmset()
        self.assertEqual(film_set.get_film_set_type(), "horror")

    @patch('builtins.input', side_effect=['horror', 'one', '1', '1', '0', 'Alone at home', 'fun',
                                          'horror', 's', '-1', '1', 's', '4', '2', 'hello'])
    def test_create_script(self, mock_input):
        film_set = wf.create_filmset()
        studio = wf.create_studio()
        script = wf.create_script(film_set, studio)

    @patch('builtins.input', side_effect=['horror', 'one', '1', '1', '0', 'Alone at home', 'fun',
                                          'horror', 's', '-1', '1', 's', '4', '2', 'hello', 'Sam', 's', '2'])
    def test_create_director(self, mock_input):
        film_set = wf.create_filmset()
        studio = wf.create_studio()
        script = wf.create_script(film_set, studio)
        director = wf.create_director(script)

    @patch('builtins.input', side_effect=['one', '1', '1', '0', "sam", 's', '45'])
    def test_create_actors(self, mock_input):
        studio = wf.create_studio()
        res = wf.create_actors(studio)
        self.assertTrue(res)

    @patch('builtins.input', side_effect=['s', 'r', 'l', 'u', 'd', 'e'])
    def test_create_shots(self, mock_input):
        camera = Camera()
        montage = Montage()
        res = wf.create_shots(camera, montage)
        self.assertTrue(res)

    @patch('builtins.input', side_effect=['s', 'del', 's', '1', 'ch', 's', '1', '1', 'e'])
    def test_make_post_production(self, mock_input):
        post_production = PostProduction()
        montage = Montage()
        res = wf.make_post_production(post_production, montage)
        self.assertTrue(res)

    @patch('builtins.input', side_effect=['horror', 'one', '1', '1', '0', 'Alone at home', 'fun',
                                          'horror', 's', '-1', '1', 's', '4', '2', 'hello', 'Sam', 's', '2'])
    def test_make_realization(self, mock_input):
        film_set = wf.create_filmset()
        studio = wf.create_studio()
        script = wf.create_script(film_set, studio)
        director = wf.create_director(script)
        post_production = PostProduction()
        montage = Montage()
        res = wf.make_realization(post_production, studio, script, director, montage)
        self.assertTrue(res)
