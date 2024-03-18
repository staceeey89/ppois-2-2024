import unittest
from datetime import datetime
from AmusementPark import AmusementPark
from Attraction import Attraction
from SecurityRequirement import SecurityRequirement
from Queue import Queue
from io import StringIO
from unittest.mock import patch
import sys
from Visitor import Visitor
from Ticket import Ticket


class TestAmusementPark(unittest.TestCase):
    def test_add_attraction(self):
        park = AmusementPark("Test Park")
        testrequirement1 = SecurityRequirement("Seat with belt")
        attraction = Attraction("Test Attraction", testrequirement1, 10)
        park.add_attraction(attraction)
        self.assertIn(attraction, park.attractions)

    def test_check_attraction_availability(self):
        park = AmusementPark("Test Park")
        attraction = Attraction("Test Attraction", "Test Requirement", 2)
        park.add_attraction(attraction)
        attraction.queue = Queue()  # Создаем очередь для аттракциона
        self.assertTrue(park.check_attraction_availability("Test Attraction"))


class TestTicket(unittest.TestCase):
    def test_ticket_creation(self):
        attraction = "Test attraction"
        cost = 100
        session_datetime = datetime.now()
        ticket_type = "Test ticket type"
        additional_info = "Test additional info"

        ticket = Ticket(attraction, cost, session_datetime, ticket_type, additional_info)

        self.assertEqual(ticket.attraction, attraction)
        self.assertEqual(ticket.price, cost)
        self.assertEqual(ticket.session_datetime, session_datetime)
        self.assertEqual(ticket.ticket_type, ticket_type)
        self.assertEqual(ticket.additional_info, additional_info)

    def test_attraction_setter(self):
        attraction = "Test attraction"
        new_attraction = "New test attraction"
        ticket = Ticket(attraction, 100, datetime.now(), "Test ticket type", "Test additional info")

        ticket.attraction = new_attraction

        self.assertEqual(ticket.attraction, new_attraction)

    def test_price_setter(self):
        attraction = "Test attraction"
        price = 100
        new_price = 200
        ticket = Ticket(attraction, price, datetime.now(), "Test ticket type", "Test additional info")

        ticket.price = new_price

        self.assertEqual(ticket.price, new_price)
class TestVisitor(unittest.TestCase):
    def test_visitor_initialization(self):
        name = "John"
        height = 180
        visitor = Visitor(name, height)
        self.assertEqual(visitor.name, name)
        self.assertEqual(visitor.height, height)

    def test_visitor_name_setter(self):
        name = "John"
        visitor = Visitor("", 0)
        visitor.name = name
        self.assertEqual(visitor.name, name)

    def test_visitor_height_setter(self):
        height = 180
        visitor = Visitor("", 0)
        visitor.height = height
        self.assertEqual(visitor.height, height)
    def test_buy_ticket(self):
        visitor = Visitor("Test Visitor", 180)
        testrequirement1 = SecurityRequirement("Seat with belt")
        attraction = Attraction("Test Attraction", testrequirement1, 2)
        ticket = Ticket(attraction, 10, datetime.now(), "Standard")
        visitor.buy_ticket(attraction, ticket)
        self.assertEqual(visitor.buy_ticket(attraction, ticket), ticket)

    @patch('builtins.input', side_effect=["2"])  # Мокируем ввод пользователя
    @patch('sys.stdout', new_callable=StringIO)  # Перехватываем вывод в консоль
    def test_choose_attraction_valid_input(self, mock_stdout, mock_input):
        visitor = Visitor("Test Visitor", 180)
        attractions = [Attraction("Attraction 1", "Requirement 1", 10), Attraction("Attraction 2", "Requirement 2", 15)]

        chosen_attraction = visitor.choose_attraction(attractions)

        # Проверяем, что выбранный аттракцион выводится в консоль
        self.assertIn("2. Attraction 2", mock_stdout.getvalue())
        # Проверяем, что метод вернул правильный аттракцион
        self.assertEqual(chosen_attraction, attractions[1])

    @patch('sys.stdout', new_callable=StringIO)
    def test_watch_rules(self, mock_stdout):
        # Создаем объекты для тестирования
        visitor = Visitor("Test Visitor", 180)
        test_requirement1 = SecurityRequirement("Keep hands and feet inside the ride")
        test_requirement2 = SecurityRequirement("Fasten seatbelt")
        attraction = Attraction("Test Attraction", test_requirement1, 10)
        attraction.add_security_requirement(test_requirement2)

        # Вызываем метод, который мы тестируем
        visitor.watch_rules(attraction)

        # Проверяем, что вывод соответствует ожидаемому
        expected_output = "Требования безопасности для данного аттракциона:\n1. Keep hands and feet inside the ride\n2. Fasten seatbelt\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)


class TestAttraction(unittest.TestCase):
    def test_add_security_requirement(self):
        attraction = Attraction("Test Attraction", "Test Requirement", 10)
        requirement = SecurityRequirement("Test Rule")
        attraction.add_security_requirement(requirement)
        self.assertIn(requirement, attraction.security_requirements)

    def test_show_security_requirements(self):
        attraction = Attraction("Test Attraction", SecurityRequirement("Test Requirement"), 10)
        test_requirement2 = SecurityRequirement("Keep hands and feet inside the ride")
        attraction.add_security_requirement(test_requirement2)

        # Перехватываем вывод в консоль
        captured_output = StringIO()
        sys.stdout = captured_output

        # Вызываем метод, который должен вывести требования безопасности
        attraction.show_security_requirements()

        # Восстанавливаем стандартный поток вывода
        sys.stdout = sys.__stdout__

        # Проверяем, что строки с требованиями безопасности были напечатаны
        printed_output = captured_output.getvalue().strip()
        expected_output = "Security requirements for Test Attraction:\nTest Requirement\nKeep hands and feet inside the ride"
        self.assertEqual(printed_output, expected_output)

class TestQueue(unittest.TestCase):
    def test_add_visitor(self):
        queue = Queue()
        visitor = Visitor("Test Visitor", 180)
        attraction1 = Attraction("Test Attraction", "Test Requirement", 2)
        queue.add_visitor(visitor, attraction1)
        self.assertIn(visitor, queue.visitors)

    def test_remove_visitor(self):
        queue = Queue()
        attraction1 = Attraction("Test Attraction", "Test Requirement", 2)
        visitor = Visitor("Test Visitor", 180)
        queue.add_visitor(visitor,attraction1)
        self.assertEqual(queue.remove_visitor(), visitor)
        with self.assertRaises(Exception):
            queue.remove_visitor()  # Очередь пуста
    def test_display_queue(self):
        # Создаем экземпляр класса Queue и добавляем некоторых посетителей
        queue = Queue()
        queue.visitors = [Visitor("Visitor1", 170), Visitor("Visitor2", 175), Visitor("Visitor3", 180)]

        # Перехватываем вывод в консоль
        captured_output = StringIO()
        sys.stdout = captured_output

        # Вызываем метод, который должен вывести очередь
        queue.display_queue()

        # Восстанавливаем стандартный поток вывода
        sys.stdout = sys.__stdout__

        # Получаем вывод, сравниваем его с ожидаемым результатом
        printed_output = captured_output.getvalue().strip()
        expected_output = "Queue:\n1. Visitor1\n2. Visitor2\n3. Visitor3"
        self.assertEqual(printed_output, expected_output)
if __name__ == '__main__':
    unittest.main()