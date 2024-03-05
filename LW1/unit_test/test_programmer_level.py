from ProgrammingLevel import ProgrammerLevel
import unittest


class TestProgrammerLevel(unittest.TestCase):
    
    def test_enum_values(self):
        self.assertEqual(ProgrammerLevel.JUNIOR.value, "Junior")
        self.assertEqual(ProgrammerLevel.MIDDLE.value, "Middle")
        self.assertEqual(ProgrammerLevel.SENIOR.value, "Senior")

    def test_enum_membership(self):
        self.assertTrue(ProgrammerLevel.JUNIOR in ProgrammerLevel)
        self.assertTrue(ProgrammerLevel.MIDDLE in ProgrammerLevel)
        self.assertTrue(ProgrammerLevel.SENIOR in ProgrammerLevel)


if __name__ == "__main__":
    unittest.main()