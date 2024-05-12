import unittest
from Project import Project
from Employee import Employee
from ITCompany import ITCompany
from Investor import Investor

class TestProject(unittest.TestCase):

    def setUp(self):
        self.test_project = Project("Test Project", 10000)

    def test_add_employee(self):
        employee = Employee("John Doe", 30, 11)
        self.test_project.add_employee(employee)
        self.assertIn(employee, self.test_project.get_employees())

    def test_receive_investment(self):
        company = ITCompany("Test Company", 100000, 'Minsk')
        initial_budget = company.get_budget()
        self.test_project.receive_investment(company, 5000)
        self.assertEqual(self.test_project.get_budget(), 15000)
        self.assertEqual(company.get_budget(), initial_budget + 5000)

    def test_add_investor(self):
        investor = Investor("Jane Smith", 10000)
        self.test_project.add_investor(investor, 5000)
        self.assertIn((investor, 5000), self.test_project.get_investments())

    def test_remove_employee(self):
        employee = Employee("John Doe", 30, 10)
        self.test_project.add_employee(employee)
        self.test_project.remove_employee(employee)
        self.assertNotIn(employee, self.test_project.get_employees())

    def test_get_info(self):
        employee1 = Employee("John Doe", 30, 1)
        employee2 = Employee("Jane Smith", 25, 6)
        investor = Investor("John Investor", 10000)
        self.test_project.add_employee(employee1)
        self.test_project.add_employee(employee2)
        self.test_project.add_investor(investor, 5000)
        expected_info = ("Проект: Test Project,\n"
                         "Бюджет: 10000,\n"
                         "Сотрудники: ['John Doe', 'Jane Smith'],\n"
                         "Ответственный за поддержку: Ответственный за поддержку не назначен,\n"
                         "Протестирован: Нет,\n"
                         "Инвесторы:\n"
                         "John Investor (5000),\n"
                         "Сумма инвестиций: 5000")
        self.assertEqual(self.test_project.get_info(), expected_info)

    def test_assign_support_employee(self):
        employee = Employee("John Doe", 30, 4)
        self.test_project.add_employee(employee)
        self.test_project.assign_support_employee(employee)
        self.assertEqual(self.test_project.get_support_employee(), employee)

    def test_test(self):
        self.assertFalse(self.test_project.get_tested())
        self.test_project.test()
        self.assertTrue(self.test_project.get_tested())

        
if __name__ == "__main__":
    unittest.main()