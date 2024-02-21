import unittest
from PostProduction import PostProduction
from Montage import Montage
from Script import Script
from Director import Director
from Studio import Studio
from Actor import Actor


class PostProductionTestCase(unittest.TestCase):

    def test_del_shot(self):
        montage = Montage()
        post_production = PostProduction()

        montage.add_shot("Первый")
        montage.add_shot("Второй")
        self.assertEqual(len(montage.get_shot_list()), 2)

        res = post_production.del_shot(1, montage)
        self.assertEqual(len(montage.get_shot_list()), 1)
        self.assertTrue(res)

        res = post_production.del_shot(-1, montage)
        self.assertFalse(res)

    def test_change_shots(self):
        montage = Montage()
        post_production = PostProduction()

        montage.add_shot("Первый")
        montage.add_shot("Второй")

        res = post_production.change_shot_place(1, 2, montage)
        self.assertTrue(res)

        res = post_production.change_shot_place(3, 2, montage)
        self.assertFalse(res)

    def test_print_shot(self):
        montage = Montage()
        post_production = PostProduction()

        montage.add_shot("Первый")
        montage.add_shot("Второй")

        res = post_production.print_list_shot(montage)
        self.assertTrue(res)

    def test_make_realization(self):
        montage = Montage()
        post_production = PostProduction()
        script = Script("Alone at home", "horror", 2, "hello", 0)
        director = Director("Billy")
        studio = Studio("one", 2)
        studio._need_young_number = 1
        studio._need_old_number = 1
        studio.add_person(Actor("Bob"))
        studio.add_person(Actor("Sam", 45))

        montage.add_shot("Первый")
        montage.add_shot("Второй")
        res = post_production.make_realization(studio, script, director, montage)
        self.assertTrue(res)

        director.change_experience(1, script)
        res = post_production.make_realization(studio, script, director, montage)
        self.assertTrue(res)

        director.change_experience(2, script)
        res = post_production.make_realization(studio, script, director, montage)
        self.assertTrue(res)
