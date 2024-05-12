import unittest
from ITCompany import ITCompany
from Employee import Employee
from Order import Order
from Project import Project
from Customer import Customer

class TestITCompany(unittest.TestCase):

    def setUp(self):
        self.company = ITCompany("Test Company", 100000, 'Minsk')

    def test_receive_investment(self):
        initial_investments = self.company.get_investments()
        self.company.receive_an_investment(5000)
        self.assertEqual(self.company.get_investments(), initial_investments + 5000)

    def test_get_employee_by_name(self):
        self.company.add_employee(Employee('John Doe', 30, 3))
        self.company.add_employee(Employee('Alice Smith', 25, 1))
        employee = self.company.get_employee_by_name('John Doe')
        self.assertIsNotNone(employee)
        self.assertEqual(employee.get_name(), 'John Doe')

    def test_mark_order_as_completed(self):
        order = Order('Order', 'Java', 1000, 100)
        self.company.add_order(order)
        self.company.mark_order_as_completed('Order')
        self.assertTrue(order.is_completed)

    def test_add_project(self):
        project = Project('Project X', 50000)
        self.company.add_project(project)
        self.assertIn(project, self.company.get_projects())

    def test_increase_budget(self):
        initial_budget = self.company.get_budget()
        self.company.increase_budget(20000)
        self.assertEqual(self.company.get_budget(), initial_budget + 20000)

    def test_remove_employee_by_name(self):
        self.company.add_employee(Employee('John Doe', 30, 2))
        self.company.remove_employee_by_name('John Doe')
        self.assertIsNone(self.company.get_employee_by_name('John Doe'))

    def test_get_info(self):
        info = self.company.get_info()
        self.assertIn('Test Company', info)
        self.assertIn('100000', info)
        self.assertIn('Minsk', info)

    def test_get_project_by_name(self):
        project = Project('Project X', 50000)
        self.company.add_project(project)
        retrieved_project = self.company.get_project_by_name('Project X')
        self.assertIsNotNone(retrieved_project)
        self.assertEqual(retrieved_project.get_proj_name(), 'Project X')

    def test_remove_project(self):
        project = Project('Project X', 50000)
        self.company.add_project(project)
        self.assertTrue(self.company.remove_project(project))
        self.assertNotIn(project, self.company.get_projects())

    def test_get_customer_by_name(self):
        customer = Customer('John Doe')
        self.company.get_client_manager().add_client(customer)
        retrieved_customer = self.company.get_customer_by_name('John Doe')
        self.assertIsNotNone(retrieved_customer)
        self.assertEqual(retrieved_customer.get_name(), 'John Doe')

    def test_get_employee(self):
        employee = Employee('John Doe', 30, 7)
        self.company.add_employee(employee)
        retrieved_employee = self.company.get_employee('John Doe')
        self.assertIsNotNone(retrieved_employee)
        self.assertEqual(retrieved_employee.get_name(), 'John Doe')


if __name__ == "__main__":
    unittest.main()