import unittest
from unittest.mock import Mock
from Check import Check

class TestCheck(unittest.TestCase):
    
    def setUp(self):
        self.mock_order = Mock()
        self.mock_order._list_order = [
            Mock(getPrice=Mock(return_value=100), getName=Mock(return_value="Item 1")),
            Mock(getPrice=Mock(return_value=200), getName=Mock(return_value="Item 2")),
            Mock(getPrice=Mock(return_value=150), getName=Mock(return_value="Item 3"))
        ]
        
    def test_generate_check_order_succeed(self):
        check = Check(self.mock_order, True)
        expected_output = [
            '======= Чек =======',
            'Статус заказа: Успешно',
            'Позиции заказа:',
            'Item 1: 100 руб.',
            'Item 2: 200 руб.',
            'Item 3: 150 руб.',
            '===================',
            'Итого: 450 руб.'
        ]
        with unittest.mock.patch('builtins.print') as mocked_print:
            check.generate_check()
            mocked_print.assert_has_calls([unittest.mock.call(output) for output in expected_output])
            
    def test_generate_check_order_fail(self):
        check = Check(self.mock_order, False)
        expected_output = [
            '======= Чек =======',
            'Статус заказа: Средств недостаточно',
            'Позиции заказа:',
            'Item 1: 100 руб.',
            'Item 2: 200 руб.',
            'Item 3: 150 руб.',
            '===================',
            'Итого: 450 руб.'
        ]
        with unittest.mock.patch('builtins.print') as mocked_print:
            check.generate_check()
            mocked_print.assert_has_calls([unittest.mock.call(output) for output in expected_output])
            
if __name__ == '__main__':
    unittest.main()
