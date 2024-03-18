from Presentation import Presentation
from Speaker import Speaker
import unittest


class TestPresentation(unittest.TestCase):
    def setUp(self):
        self.speaker = Speaker("Игорь Джабраилов", "БГУИР","Квантовая физика","Сеньор", "12:00")
        self.presentation = Presentation("Квантовая физика", self.speaker, "Квантовая физика простым языком")

    def test_init(self):
        self.assertEqual(self.presentation.get_title(), "Квантовая физика")
        self.assertEqual(self.presentation.get_speaker(), self.speaker)
        self.assertEqual(self.presentation.get_topic(), "Квантовая физика простым языком")

    def test_set_title(self):
        self.presentation.set_title("Теория музыки")
        self.assertEqual(self.presentation.get_title(), "Теория музыки")

        self.presentation.set_title(1123)
        assert self.presentation.get_title != self.presentation.set_title

    def test_set_speaker(self):
        new_speaker = Speaker("Надежда Джабраилова", "БГУ","Джаз","Джуниор", "10:00")
        self.presentation.set_speaker(new_speaker)
        self.assertEqual(self.presentation.get_speaker(), new_speaker)

    def test_set_topic(self):
        self.presentation.set_topic("New Topic")
        self.assertEqual(self.presentation.get_topic(), "New Topic")

        self.presentation.set_topic(2)
        assert self.presentation.get_topic != self.presentation.set_topic

    def test_add_slide(self):
        self.presentation.add_slide("Slide 1")
        self.assertIn("Slide 1", self.presentation._Presentation__slides)


if __name__ == '__main__':
    unittest.main()
