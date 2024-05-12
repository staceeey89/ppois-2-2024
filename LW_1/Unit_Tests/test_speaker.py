from Speaker import Speaker
import unittest


class TestSpeaker(unittest.TestCase):
    def setUp(self):
        self.speaker = Speaker("Иван", "Компания А", "Тема", "Джуниор", "Утро")

    def test_constructor(self):
        self.assertEqual(self.speaker.get_name(), "Иван")
        self.assertEqual(self.speaker.get_affiliation(), "Компания А")
        self.assertEqual(self.speaker.get_presentation_topic(), "Тема")
        self.assertEqual(self.speaker.get_experience_level(), "Джуниор")
        self.assertEqual(self.speaker.get_preferred_time(), "Утро")
        self.assertEqual(self.speaker.average_rating(), None)

    def test_set_presentation_topic(self):
        self.speaker.set_presentation_topic("Новая тема")
        self.assertEqual(self.speaker.get_presentation_topic(), "Новая тема")

        #️with self.assertRaises(ValueError):
        #️    self.speaker.set_presentation_topic(123)

    def test_set_experience_level(self):
        self.speaker.set_experience_level("Мидл")
        self.assertEqual(self.speaker.get_experience_level(), "Мидл")

        #️with self.assertRaises(ValueError):
        #️    self.speaker.set_experience_level("Стажер")

    def test_set_preferred_time(self):
        self.speaker.set_preferred_time("Вечер")
        self.assertEqual(self.speaker.get_preferred_time(), "Вечер")

        #️with self.assertRaises(ValueError):
        #️    self.speaker.set_preferred_time(123)

    def test_average_rating(self):
        self.assertEqual(self.speaker.average_rating(), None)
        self.speaker._Speaker__presentation_ratings = [4, 5, 3, 4, 5]
        self.assertEqual(self.speaker.average_rating(), 4.2)

    def test_display_info(self):
        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output
        self.speaker.display_info()
        sys.stdout = sys.__stdout__
        expected_output = """Имя: Иван
Членство: Компания А
Тема презентации: Тема
Уровень опыта: Джуниор
Предпочтительное время: Утро
Средняя оценка: None
Рейтинги презентаций:
Обзоры презентаций:
"""
        self.assertEqual(captured_output.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
