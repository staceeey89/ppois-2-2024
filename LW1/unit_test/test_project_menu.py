import unittest
from unittest.mock import patch
from ITCompany import ITCompany
from Project import Project
from ProjectMenu import ProjectMenu
from Employee import Employee


class TestProjectMenu(unittest.TestCase):
    @patch('builtins.input', side_effect=['7'])
    def test_project_menu(self, mock_input):
        company = ITCompany("Test Company", 10000000, 'Minsk')
        project = Project("Test Project", 1000)
        ProjectMenu.project_menu(company, project)
        ProjectMenu.load_state()
        self.assertEqual(mock_input.call_count, 1)

    @patch('builtins.input', side_effect=['1', 'Test Employee', '7'])
    def test_project_menu_add_employee(self, mock_input):
        company = ITCompany("Test Company", 10000000, 'Minsk')
        project = Project("Test Project", 1000)
        company.add_employee(Employee("Test Employee", 20, 1))
        ProjectMenu.project_menu(company, project)
        self.assertEqual(mock_input.call_count, 3)

    @patch('builtins.input', side_effect=['2', 'Test Employee', '7'])
    def test_project_menu_assign_support_employee(self, mock_input):
        company = ITCompany("Test Company", 10000000, 'Minsk')
        project = Project("Test Project", 1000)
        company.add_employee(Employee("Test Employee", 20, 1))
        ProjectMenu.project_menu(company, project)
        self.assertEqual(mock_input.call_count, 3)

    @patch('builtins.input', side_effect=['3', '7'])
    def test_project_menu_test(self, mock_input):
        company = ITCompany("Test Company", 10000000, 'Minsk')
        project = Project("Test Project", 1000)
        ProjectMenu.project_menu(company, project)
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input', side_effect=['4', '7'])
    def test_project_menu_print_info(self, mock_input):
        company = ITCompany("Test Company", 10000000, 'Minsk')
        project = Project("Test Project", 1000)
        ProjectMenu.project_menu(company, project)
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input', side_effect=['5', '7'])
    def test_project_menu_remove_project(self, mock_input):
        company = ITCompany("Test Company", 10000000, 'Minsk')
        project = Project("Test Project", 1000)
        company.add_project(project)
        ProjectMenu.project_menu(company, project)
        self.assertEqual(mock_input.call_count, 1)


if __name__ == "__main__":
    unittest.main()