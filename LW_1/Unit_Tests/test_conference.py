from Conference import Conference
from datetime import datetime, timedelta
from Person import Person
from Presentation import Presentation
from Speaker import Speaker
import unittest

class TestConference(unittest.TestCase):
    def setUp(self):
        self.start_date = datetime.now()
        self.end_date = self.start_date + timedelta(days=3)
        self.application_deadline = self.start_date - timedelta(days=1)
        self.coffee_breaks = [('10:30', '10:45'), ('14:00', '14:15')]
        self.lunch_break = ('12:00', '13:00')
        self.conference = Conference("Тестовая конференция", "Тестовое место проведения", self.start_date, self.end_date, 100, self.application_deadline, self.coffee_breaks, self.lunch_break)

        self.participant = Person("Иванов Иван",'БГУИР')
        self.speaker = Speaker("Петров Петр", "БНТУ","Физика","Сеньор","10:00")
        self.presentation = Presentation("Квантовая физика", self.speaker, "Квантовая физика простым языком")

    def test_getters(self):
        self.assertEqual(self.conference.get_name(), "Тестовая конференция")
        self.assertEqual(self.conference.get_location(), "Тестовое место проведения")
        self.assertEqual(self.conference.get_start_date(), self.start_date)
        self.assertEqual(self.conference.get_end_date(), self.end_date)
        self.assertEqual(self.conference.get_max_participants(), 100)
        self.assertEqual(self.conference.get_application_deadline(), self.application_deadline)
        self.assertEqual(self.conference.get_coffee_breaks(), self.coffee_breaks)
        self.assertEqual(self.conference.get_lunch_break(), self.lunch_break)

    def test_setters(self):
        new_name = "Тестовая конференция"
        self.conference.set_name(new_name)
        self.assertEqual(self.conference.get_name(), new_name)

        new_location = "Тестовое место проведения"
        self.conference.set_location(new_location)
        self.assertEqual(self.conference.get_location(), new_location)

        new_start_date = self.start_date
        self.conference.set_start_date(new_start_date)
        self.assertEqual(self.conference.get_start_date().date(), new_start_date.date())

        new_end_date = self.end_date
        self.conference.set_end_date(new_end_date)
        self.assertEqual(self.conference.get_end_date().date(), new_end_date.date())

        new_max_participants = 150
        self.conference.set_max_participants(new_max_participants)
        self.assertEqual(self.conference.get_max_participants(), new_max_participants)

        new_application_deadline = self.application_deadline + timedelta(days=1)
        self.conference.set_application_deadline(new_application_deadline)
        self.assertEqual(self.conference.get_application_deadline().date(), new_application_deadline.date())

        new_coffee_breaks = [('11:00', '11:15'), ('15:00', '15:15')]
        self.conference.set_coffee_breaks(new_coffee_breaks)
        self.assertEqual(self.conference.get_coffee_breaks(), new_coffee_breaks)

        new_lunch_break = ('13:30', '14:30')
        self.conference.set_lunch_break(new_lunch_break)
        self.assertEqual(self.conference.get_lunch_break(), new_lunch_break)

    def test_add_participant(self):
        self.conference.add_participant(self.speaker)
        self.assertIn(self.speaker, self.conference._Conference__participants)

    def test_select_presentation(self):
        self.conference.select_presentation(self.presentation)
        self.assertIn(self.presentation, self.conference._Conference__presentations)

    def test_add_presentation(self):
        self.conference.add_participant(self.speaker)
        self.conference.add_presentation("Квантовая физика", self.speaker, "Квантовая физика простым языком")
        presentations = self.conference._Conference__presentations
        self.assertTrue(any(presentation.get_title() == "Квантовая физика" for presentation in presentations))
        self.assertTrue(any(presentation.get_topic() == "Квантовая физика простым языком" for presentation in presentations))

    def test_add_presentation_for_unregistered_speaker(self):
        speaker1 = Speaker("Игорь", "БГУИР", "Тема", "Джуниор", "Вечер")
        self.assertFalse(self.conference.add_presentation("Музыка", speaker1, "Классическая музыка"))

    def test_prepare_conference_with_all_resources(self):
        self.assertTrue(self.conference.prepare_conference())

    def test_conduct_conference_after_preparation(self):
        self.conference.prepare_conference()
        self.assertIsNone(self.conference.conduct_conference())

    def test_collect_feedback(self):
        self.conference.add_participant(self.speaker)
        self.conference.add_presentation("Квантовая физика", self.speaker, "Квантовая физика простым языком")
        feedback = self.conference.collect_feedback()
        self.assertIsInstance(feedback, dict)

    def test_notify_participants(self):
        self.assertIsNone(self.conference.notify_participants("Текст сообщения"))

    def test_generate_schedule(self):
        self.conference.add_participant(self.speaker)
        self.conference.add_presentation("Квантовая физика", self.speaker, "Квантовая физика простым языком")
        schedule = self.conference.organize_program()
        self.assertIsInstance(schedule, dict)
        self.assertTrue(schedule)

    def test_handle_unprepared_speaker(self):
        speaker1 = Speaker("Иванов", "МГУ", "Физика", "Профессор", "Утро")
        self.assertIsNone(self.conference.handle_unprepared_speaker(speaker1))

if __name__ == '__main__':
    unittest.main()