import unittest
from ProgrammingLanguage import ProgrammingLanguage


class TestProgrammingLanguage(unittest.TestCase):

    def test_enum_values(self):
        self.assertEqual(ProgrammingLanguage.CPP.value, "C++")
        self.assertEqual(ProgrammingLanguage.C_SHARP.value, "C#")
        self.assertEqual(ProgrammingLanguage.PYTHON.value, "Python")
        self.assertEqual(ProgrammingLanguage.JAVA.value, "Java")
        self.assertEqual(ProgrammingLanguage.HTML.value, "HTML")
        self.assertEqual(ProgrammingLanguage.PHP.value, "PHP")
        self.assertEqual(ProgrammingLanguage.MYSQL.value, "MySQL")

    def test_enum_membership(self):
        self.assertTrue(ProgrammingLanguage.CPP in ProgrammingLanguage)
        self.assertTrue(ProgrammingLanguage.C_SHARP in ProgrammingLanguage)
        self.assertTrue(ProgrammingLanguage.PYTHON in ProgrammingLanguage)
        self.assertTrue(ProgrammingLanguage.JAVA in ProgrammingLanguage)
        self.assertTrue(ProgrammingLanguage.HTML in ProgrammingLanguage)
        self.assertTrue(ProgrammingLanguage.PHP in ProgrammingLanguage)
        self.assertTrue(ProgrammingLanguage.MYSQL in ProgrammingLanguage)

if __name__ == "__main__":
    unittest.main()