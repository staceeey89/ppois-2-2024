
from unittest import TestCase
from ITCompany import ITCompany
import unittest

class CompanyTest(TestCase):
    def setUp(self):
        self.company = ITCompany("Test Company", 100000, 'Minsk')

    def test_change_name(self):
        self.company.set_name('OSTIS')
        expected_name = 'OSTIS'
        assert self.company.get_name() == expected_name

    def test_fill_emps(self):
        employee = ('Nikolai', 23, 4, 1900)
        expected_value=1
        self.company.add_employee(employee)
        assert self.company.get_num_of_emps() == expected_value

if __name__ == "__main__":
    unittest.main()