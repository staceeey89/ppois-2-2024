import unittest
from CompanyCreator import CompanyCreator
import os
from unittest.mock import patch

class TestCompanyCreator(unittest.TestCase):

    @patch('builtins.input', side_effect=['Test Company', '100000', 'Minsk'])
    def test_create_company(self, mock_input):
        company = CompanyCreator.create_company()
        self.assertEqual(company.get_name(), 'Test Company')
        self.assertEqual(company.get_budget(), 100000)
        self.assertEqual(company.get_location(), 'Minsk')

    @patch('builtins.input', side_effect=['test_file'])
    def test_delete_company_file_exists(self, mock_input):
        with open('test_file', 'w') as f:
            f.write('test')

        CompanyCreator.delete_company('test_file')
        self.assertFalse(os.path.exists('test_file'))


if __name__ == "__main__":
    unittest.main()