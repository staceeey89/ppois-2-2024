import unittest
from datetime import datetime, timedelta

from src.event import Call, Crime
from src.investigation import Investigation
from src.law import Law
from src.officer import Officer, Detective, PatrolOfficer, OfficerGenerator, Rank, Position
from src.public_security import PublicSecurity


class TestOfficerClasses(unittest.TestCase):
    def setUp(self):
        self.rank = Rank.CAPTAIN
        self.experience = 10
        self.unavailable_until = datetime(2024, 2, 21)
        self.fullname = "John Doe"

    def test_officer_str(self):
        officer = Officer(self.fullname, self.rank, self.experience, self.unavailable_until)
        self.assertEqual(str(officer),
                         "  Officer         John Doe             Captain              ★10        2024-02-21 00:00:00")

    def test_detective_str(self):
        detective = Detective(self.fullname, self.rank, self.experience, self.unavailable_until)
        self.assertEqual(str(detective),
                         "🕵️Detective       John Doe             Captain              ★10        2024-02-21 00:00:00")

    def test_patrol_officer_str(self):
        patrol_officer = PatrolOfficer(self.fullname, self.rank, self.experience, self.unavailable_until)
        self.assertEqual(str(patrol_officer),
                         "👮Patrol Officer  John Doe             Captain              ★10        2024-02-21 00:00:00")

    def test_officer_generator(self):
        officer = OfficerGenerator(self.fullname, Position.PATROL, self.rank, self.experience, self.unavailable_until)
        self.assertIsInstance(officer, PatrolOfficer)
        self.assertEqual(str(officer),
                         "👮Patrol Officer  John Doe             Captain              ★10        2024-02-21 00:00:00")

        officer = OfficerGenerator(self.fullname, Position.DETECTIVE, self.rank, self.experience,
                                   self.unavailable_until)
        self.assertIsInstance(officer, Detective)
        self.assertEqual(str(officer),
                         "🕵️Detective       John Doe             Captain              ★10        2024-02-21 00:00:00")

        officer = OfficerGenerator(self.fullname, Position.PATROL, Rank.CONSTABLE, self.experience,
                                   self.unavailable_until)
        self.assertIsInstance(officer, PatrolOfficer)
        self.assertEqual(str(officer),
                         "👮Patrol Officer  John Doe             Constable            ★10        2024-02-21 00:00:00")

        officer = OfficerGenerator(self.fullname, Position.DETECTIVE, Rank.CONSTABLE, self.experience,
                                   self.unavailable_until)
        self.assertIsInstance(officer, Detective)
        self.assertEqual(str(officer),
                         "🕵️Detective       John Doe             Constable            ★10        2024-02-21 00:00:00")


class TestRankEnum(unittest.TestCase):
    def test_from_string(self):
        self.assertEqual(Rank.from_string("Constable"), Rank.CONSTABLE)
        self.assertEqual(Rank.from_string("Sergeant"), Rank.SERGEANT)
        self.assertEqual(Rank.from_string("Lieutenant"), Rank.LIEUTENANT)
        self.assertEqual(Rank.from_string("Captain"), Rank.CAPTAIN)
        self.assertEqual(Rank.from_string("Inspector"), Rank.INSPECTOR)
        self.assertEqual(Rank.from_string("Chief Inspector"), Rank.CHIEF_INSPECTOR)
        self.assertEqual(Rank.from_string("Superintendent"), Rank.SUPERINTENDENT)
        self.assertEqual(Rank.from_string("Deputy Chief"), Rank.DEPUTY_CHIEF)
        self.assertEqual(Rank.from_string("Chief"), Rank.CHIEF)
        self.assertEqual(Rank.from_string("constable"), None)

    def test_to_string(self):
        self.assertEqual(str(Rank.CONSTABLE), "Constable")
        self.assertEqual(str(Rank.SERGEANT), "Sergeant")
        self.assertEqual(str(Rank.LIEUTENANT), "Lieutenant")
        self.assertEqual(str(Rank.CAPTAIN), "Captain")
        self.assertEqual(str(Rank.INSPECTOR), "Inspector")
        self.assertEqual(str(Rank.CHIEF_INSPECTOR), "Chief Inspector")
        self.assertEqual(str(Rank.SUPERINTENDENT), "Superintendent")
        self.assertEqual(str(Rank.DEPUTY_CHIEF), "Deputy Chief")
        self.assertEqual(str(Rank.CHIEF), "Chief")


class TestPositionEnum(unittest.TestCase):
    def test_from_string(self):
        self.assertEqual(Position.from_string("Detective"), Position.DETECTIVE)
        self.assertEqual(Position.from_string("Patrol Officer"), Position.PATROL)


class TestPublicSecurity(unittest.TestCase):
    def setUp(self):
        self.rank = Rank.CAPTAIN
        self.experience = 10
        self.unavailable_until = datetime(2024, 2, 21)
        self.fullname = "John Doe"
        self.officer = Officer(self.fullname, self.rank, self.experience, self.unavailable_until)
        self.call = Call("Title", "Description", 5, "hard", "Address")
        self.assigned_officers = [self.officer]

    def test_public_security_operation(self):
        public_security = PublicSecurity(self.call, self.assigned_officers)
        timenow = datetime.now()
        public_security.public_security_operation(timenow)
        self.assertEqual(self.officer.unavailable_until, timenow + timedelta(minutes=315))

    def test_str(self):
        public_security = PublicSecurity(self.call, self.assigned_officers)
        expected_str = str(self.officer)
        self.assertEqual(str(public_security), expected_str)


class TestLaw(unittest.TestCase):
    def setUp(self):
        self.title = "Speeding"
        self.jurisdiction = "Traffic"
        self.description = "Exceeding the speed limit"
        self.penalty = "Fine or License Suspension"
        self.law = Law(self.title, self.jurisdiction, self.description, self.penalty)

    def test_str(self):
        expected_str = f"{self.title} - {self.penalty}"
        self.assertEqual(str(self.law), expected_str)

    def test_attributes(self):
        self.assertEqual(self.law.name, self.title)
        self.assertEqual(self.law.jurisdiction, self.jurisdiction)
        self.assertEqual(self.law.description, self.description)
        self.assertEqual(self.law.penalty, self.penalty)


class TestInvestigation(unittest.TestCase):
    def setUp(self):
        self.crime = Crime("Theft", "Robbery", 5, "hard", Law("",
                                                              "", "", ""))
        self.officer = Officer("John Doe", Rank.CONSTABLE, 10, datetime.now())
        self.assigned_officers = [self.officer]
        self.investigation = Investigation(self.crime, self.assigned_officers)
        self.timenow = datetime.now()

    def test_investigate(self):
        self.investigation.investigate(self.timenow)
        expected_until = self.timenow + timedelta(hours=504)
        self.assertEqual(self.investigation.until, expected_until)
        for officer in self.assigned_officers:
            self.assertEqual(officer.unavailable_until, expected_until)

    def test_law(self):
        self.assertEqual(self.investigation.law, str(self.crime.law))

    def test_str(self):
        expected_str = str(self.crime)
        self.assertEqual(str(self.investigation), expected_str)


class TestDuty(unittest.TestCase):
    def setUp(self):
        self.timenow = datetime.now()


if __name__ == '__main__':
    unittest.main()
