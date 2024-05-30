import unittest

from student import Student, is_valid_name
from exam_system import ExamSystem
from exam import Exam
from additional_classes import AdditionalClasses
from learning_material import LearningMaterial


class TestStudent(unittest.TestCase):

    def test_is_valid_name(self):
        self.assertTrue(is_valid_name('Иван'))
        self.assertTrue(is_valid_name('Иванов'))
        self.assertFalse(is_valid_name('123'))
        self.assertFalse(is_valid_name('Ива#ов'))

    def test_student_init(self):
        student = Student('Иван', 'Иванов', '123456')
        self.assertEqual(student.first_name, 'Иван')
        self.assertEqual(student.last_name, 'Иванов')
        self.assertEqual(student.group, '123456')
        self.assertEqual(len(student.exams), 0)
        self.assertEqual(student.resits, 0)
        self.assertEqual(len(student.learning_materials), 0)
        self.assertEqual(len(student.additional_classes), 0)
        self.assertEqual(len(student.consultations), 0)

    def test_validate_group_number(self):
        self.assertRaises(ValueError, Student.validate_group_number, '123')
        self.assertRaises(ValueError, Student.validate_group_number, '12345678')
        Student.validate_group_number('123456')

    def test_add_exam(self):
        student = Student('Иван', 'Иванов', '123456')
        exam = Exam('Математика', [5, 4, 3])
        student.add_exam(exam)
        self.assertIn(exam, student.exams.values())

    def test_add_learning_material(self):
        student = Student('Иван', 'Иванов', '123456')
        learning_material = LearningMaterial('Математика', 'Теория чисел')
        student.add_learning_material(learning_material)
        self.assertIn(learning_material, student.learning_materials)

    def test_attend_additional_class(self):
        student = Student('Иван', 'Иванов', '123456')
        additional_class = AdditionalClasses('Математика', '12.12.2022')
        student.attend_additional_class(additional_class)
        self.assertIn(additional_class, student.additional_classes)


class TestExamSystem(unittest.TestCase):
    def setUp(self):
        self.exam_system = ExamSystem()

    def test_add_student(self):
        student = Student("Иван", "Иванов", "123456")
        self.exam_system.add_student(student)
        self.assertIn(student, self.exam_system.students)

    def test_get_student(self):
        student = Student("Иван", "Иванов", "123456")
        self.exam_system.add_student(student)
        self.assertEqual(self.exam_system.get_student("Иван", "Иванов"), student)

    def test_delete_student(self):
        student = Student("Иван", "Иванов", "123456")
        self.exam_system.add_student(student)
        self.exam_system.delete_student("Иван", "Иванов")
        self.assertNotIn(student, self.exam_system.students)


class TestExam(unittest.TestCase):
    def setUp(self):
        self.exam = Exam("Математика", 3)

    def test_add_score(self):
        self.exam.add_score(4)
        self.assertIn(4, self.exam.scores)

    def test_last_score(self):
        self.exam.add_score(4)
        self.assertEqual(self.exam.last_score(), 4)

    def test_has_passed(self):
        self.exam.add_score(4)
        self.assertTrue(self.exam.has_passed())


class TestAdditionalClasses(unittest.TestCase):
    def test_is_valid_date(self):
        self.assertTrue(AdditionalClasses.is_valid_date("01.01.2022"))
        self.assertFalse(AdditionalClasses.is_valid_date("01.13.2022"))


class TestLearningMaterial(unittest.TestCase):
    def test_use_for_preparation(self):
        learning_material = LearningMaterial("Математика", "Теория")
        learning_material.use_for_preparation()


if __name__ == "__main__":
    unittest.main()

