#  coverage html
#  coverage report -m
#  coverage run -m unittest discover
from unittest.mock import MagicMock
import unittest

from Student_Model.group import Group
from Student_Model.student import Student
from Student_Model.exam import Exam
from Student_Model.exam import Schedule


class TestGroup(unittest.TestCase):

    def setUp(self):
        self.group = Group("Test group")
        self.student = MagicMock(spec=Student)

    def test_add_student(self):
        # Test adding a student to the group
        self.group.add_student(self.student)
        self.assertIn(self.student, self.group.get_list_of_students())

    def test_expel_student(self):
        # Test expelling a student from the group
        self.group.add_student(self.student)
        self.group.expel_student(0)
        self.assertNotIn(self.student, self.group.get_list_of_students())

    def test_get_name(self):
        # Test getting name of the group
        self.assertEqual("Test group", self.group.get_name())

    def test_add_exam(self):
        # Test adding exam to the group
        exam = MagicMock(spec=Exam)
        self.group.add_exam(exam)
        self.assertIn(exam, self.group.get_list_of_exams())


class TestExam(unittest.TestCase):

    def setUp(self):
        self.exam = Exam("Test exam", "2024-06-14", "09:00")

    def test_get_name(self):
        # Test getting name of the exam
        self.assertEqual("Test exam", self.exam.get_name())

    def test_get_schedule_by_date(self):
        # Test getting schedule by date
        schedule = Schedule("2024-06-14", "09:00")
        self.assertEqual(schedule.get_date(), self.exam.get_schedule().get_date())

    def test_get_schedule_by_time(self):
        # Test getting schedule by time
        schedule = Schedule("2024-06-14", "09:00")
        self.assertEqual(schedule.get_time(), self.exam.get_schedule().get_time())


class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student("Maximkov Maxim Maximovich")

    def test_get_name(self):
        # Test getting name of the student
        self.assertEqual("Maximkov Maxim Maximovich", self.student.get_name())


if __name__ == '__main__':
    unittest.main()
