import unittest
from unittest.mock import MagicMock, patch
from Visitor import Visitor
from Attraction import Attraction
from Ticket import Ticket
from SecurityRequirement import SecurityRequirement
from Queue import Queue


class TestVisitor(unittest.TestCase):

    @patch('builtins.input', side_effect=["John", "170", "70", "25"])
    def test_get_visitor_info_valid_input(self, mock_input):
        visitor = Visitor()
        visitor.get_visitor_info()
        self.assertEqual(visitor.name, "John")
        self.assertEqual(visitor.height, 170)
        self.assertEqual(visitor.weight, 70)
        self.assertEqual(visitor.age, 25)

    @patch('builtins.input', side_effect=["1", "2", "2", "2", "2"])
    def test_buy_ticket(self, mock_input):
        visitor = Visitor("John")
        park = MockPark()
        queue = MockQueue()

        visitor.buy_ticket(park, queue)

        # Assert that the number of tickets matches the input
        self.assertEqual(len(visitor.tickets), 2)

        # Assert that the selected attraction is in the tickets
        self.assertTrue(visitor.tickets[0].attraction in park.attractions)

    @patch('builtins.input', side_effect=["1"])
    def test_choose_attraction_valid_choice(self, mock_input):
        # Создание фиктивных объектов парка, аттракционов и очереди
        attraction = Attraction("Rollercoaster", 10)
        park = MagicMock()
        park.attractions = [attraction]
        queue = Queue()

        # Создание фиктивных требований безопасности
        security_requirement = SecurityRequirement("wear belt", 150, 70, 12)
        attraction.security_requirements = [security_requirement]

        # Создание фиктивного билета
        ticket = Ticket(attraction)

        # Создание фиктивного посетителя
        visitor = Visitor("John", 160, 65, 20)
        visitor.tickets = [ticket]  # Добавляем фиктивный билет в список билетов посетителя

        # Моделирование вызова метода visit_attraction
        visitor.visit_attraction = MagicMock()

        # Вызов тестируемого метода
        visitor.choose_attraction(park)

        # Проверка вызова метода visit_attraction с выбранным аттракционом
        visitor.visit_attraction.assert_called_once_with(attraction)

    def test_watch_rules_valid_choice(self):
        # Создание фиктивных объектов парка и аттракционов
        attraction = Attraction("Rollercoaster", 10)
        park = MagicMock()
        park.attractions = [attraction]

        # Создание фиктивных требований безопасности
        security_requirement = SecurityRequirement("wear belt", 150, 70, 12)
        attraction.security_requirements = [security_requirement]

        # Создание фиктивного посетителя
        visitor = Visitor()

        # Моделирование ввода пользователя
        with patch('builtins.input', side_effect=["1"]):
            with patch('builtins.print') as mock_print:
                visitor.watch_rules(park)

        # Проверка вызовов функций print
        mock_print.assert_called_with(
            "1. wear belt  Min Height: 150, Max Weight: 70 Min Age: 12"
        )

    @patch('builtins.print')  # Mock the print function
    def test_watch_tickets(self, mock_print):
        # Create a visitor with mock tickets
        visitor = Visitor()
        visitor.tickets = [
            Ticket(Attraction("Rollercoaster", 10)),
            Ticket(Attraction("Ferris Wheel", 10)),
            Ticket(Attraction("Rollercoaster", 10))
        ]

        # Call the method
        visitor.watch_tickets()

        # Check if the correct messages were printed
        expected_messages = [
            "My purchased tickets :",
            "1. Rollercoaster - 2 ticket/s",
            "2. Ferris Wheel - 1 ticket/s"
        ]
        printed_messages = [call[0][0] for call in mock_print.call_args_list]  # Extract printed messages
        self.assertEqual(expected_messages, printed_messages)


class MockPark:
    def __init__(self):
        self.attractions = [
            MockAttraction("Roller Coaster"),
            MockAttraction("Ferris Wheel")
        ]

class MockAttraction:
    def __init__(self, name):
        self.name = name

class MockQueue:
    def join_queue_ticket(self):
        pass

if __name__ == '__main__':
    unittest.main()
