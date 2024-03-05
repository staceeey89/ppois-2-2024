import unittest
from Employee import Employee
from unittest import TestCase
from Project import Project

class EmployeeTest(TestCase):

    def setUp(self):
        self.employee = Employee('John Doe', 30, 10)
        self.project = Project('Project X', 10000)

    def test_salary(self):
        self.employee = Employee('Nikolai', 23, 4, 1900)
        self.employee.set_salary(1000)
        expected_salary = 1000
        assert self.employee.get_salary() == expected_salary

    def test_assign_project(self):
        self.employee.assign_project(self.project)
        assert self.employee.get_project() == self.project

    def test_get_info(self):
        self.employee.get_info()
        self.employee.__str__()
        assert self.employee.get_name() != 'Ivan Doe'


if __name__ == "__main__":
    unittest.main()