from Scientist import Scientist
import unittest


class TestScientist(unittest.TestCase):
    def setUp(self):
        self.scientist = Scientist("Иван", "Институт А", "Физика")

    def test_constructor(self):
        self.assertEqual(self.scientist.get_name(), "Иван")
        self.assertEqual(self.scientist.get_affiliation(), "Институт А")
        self.assertEqual(self.scientist.get_field_of_study(), "Физика")
        self.assertEqual(self.scientist.get_collaborations(), [])
        self.assertEqual(self.scientist.get_contacts(), {})
        self.assertEqual(self.scientist.get_achievements(), [])
        self.assertEqual(self.scientist._Scientist__research_publications, [])
        self.assertEqual(self.scientist._Scientist__grant_proposals, [])
        self.assertEqual(self.scientist._Scientist__conferences_attended, [])

    def test_set_field_of_study(self):
        self.scientist.set_field_of_study("Химия")
        self.assertEqual(self.scientist.get_field_of_study(), "Химия")

        self.scientist.set_field_of_study(123)
        assert self.scientist.get_field_of_study != self.scientist.set_field_of_study

    def test_publish_research(self):
        self.scientist.publish_research("Название исследования")
        self.assertIn("Название исследования", self.scientist._Scientist__research_publications)

    def test_write_grant_proposal(self):
        self.scientist.write_grant_proposal("Название гранта")
        self.assertIn("Название гранта", self.scientist._Scientist__grant_proposals)

    def test_attend_conference(self):
        self.scientist.attend_conference("Название конференции")
        self.assertIn("Название конференции", self.scientist._Scientist__conferences_attended)

    def test_collaborate_with(self):
        other_scientist = Scientist("Петр", "Институт Б", "Биология")
        self.scientist.collaborate_with(other_scientist)
        self.assertIn(other_scientist, self.scientist.get_collaborations())

    def test_track_achievements(self):
        self.scientist.track_achievements("Достижение")
        self.assertIn("Достижение", self.scientist.get_achievements())


    def test_subscribe_to_journals(self):
        journal_list = ["Журнал 1", "Журнал 2", "Журнал 3"]
        self.scientist.subscribe_to_journals(journal_list)
        self.assertListEqual(journal_list, self.scientist.get_subscribed_journals())


if __name__ == '__main__':
    unittest.main()
