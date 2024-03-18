import unittest
from OrganizingCommittee import OrganizingCommittee

class TestOrganizingCommittee(unittest.TestCase):
    def setUp(self):
        self.committee = OrganizingCommittee("Иванов", ["Петров", "Сидоров"])

    def test_constructor(self):
        self.assertEqual(self.committee.get_chairperson(), "Иванов")
        self.assertEqual(self.committee.get_members(), ["Петров", "Сидоров"])

    def test_set_chairperson(self):
        self.committee.set_chairperson("Петров")
        self.assertEqual(self.committee.get_chairperson(), "Петров")

        self.committee.set_chairperson(123)
        assert self.committee.get_chairperson != self.committee.set_members

    def test_set_members(self):
        self.committee.set_members(["Сидоров", "Петров", "Иванов"])
        self.assertEqual(self.committee.get_members(), ["Сидоров", "Петров", "Иванов"])

        self.committee.set_members(125)
        assert self.committee.get_members != self.committee.set_members

    def test_add_member(self):
        self.committee.add_member("Джабраилов")
        self.assertIn("Джабраилов", self.committee.get_members())

    def test_remove_member(self):
        self.committee.remove_member("Сидоров")
        self.assertNotIn("Сидоров", self.committee.get_members())

    def test_remove_non_existing_member(self):
        with self.assertRaises(ValueError) as context:
            self.committee.remove_member("Давид")
        self.assertEqual(str(context.exception), "Удаляемый член комитета не найден.")

if __name__ == '__main__':
    unittest.main()
