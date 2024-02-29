import unittest
from unittest.mock import patch
from Studio import Studio
from Script import Script
from Actor import Actor


class StudioTestCase(unittest.TestCase):

    def test_getters_studio(self):
        studio = Studio("first", 5)
        self.assertEqual(studio.get_name(), "first")
        self.assertEqual(studio.get_person_number(), 5)
        self.assertEqual(len(studio.get_list_young_persons()), 0)
        self.assertEqual(len(studio.get_list_old_persons()), 0)

    @patch('builtins.input', side_effect=['Alice', '30', 'Dad', '12', 'Bob', '45', 'Sasha', 's', 'Charlie', '50'])
    def test_set_number_actor_helper(self, mock_input):
        studio = Studio("first", 3)  # Создаем экземпляр вашего класса
        studio._need_old_number = 2  # Устанавливаем значения для теста
        studio._need_young_number = 1
        studio._person_number = 3

        res = studio.set_number_actor_helper()  # Вызываем функцию, которую тестируем

        # Проверяем, что список старых и молодых актеров заполнен правильно
        self.assertTrue(res)
        self.assertEqual(len(studio._list_old_persons), 2)
        self.assertEqual(len(studio._list_young_persons), 1)

    @patch('builtins.input', side_effect=['s', '2', '0', '1', '0'])
    def test_set_non_equally_number_people(self, mock_input):
        script = Script("first", "horror", 1, "hello", 0)
        studio = Studio("first", 1)
        studio._need_old_number = 1
        studio._need_young_number = 0
        studio._person_number = 1

        res = studio.set_number_people(1, script)
        self.assertFalse(res)

        res = studio.set_number_people(-1, script)
        self.assertFalse(res)

    @patch('builtins.input', side_effect=['1', '0', 'John Doe', '45'])
    def test_set_true_number_people(self, mock_input):
        script = Script("first", "horror", 1, "hello", 0)
        studio = Studio("first", 1)
        studio._need_old_number = 1
        studio._need_young_number = 0
        studio._person_number = 1

        res = studio.set_number_people(1, script)
        self.assertTrue(res)

    def test_set_young_old_numbers(self):
        studio = Studio("first", 1)
        studio._need_old_number = 1
        studio._need_young_number = 0
        studio._person_number = 1
        studio.add_person(Actor("Sasha"))

        res = studio.set_young_old_numbers(1, 0)
        self.assertTrue(res)

        res = studio.set_young_old_numbers(1, 1)
        self.assertFalse(res)
