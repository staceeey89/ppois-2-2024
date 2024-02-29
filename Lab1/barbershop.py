from client import Client
from barber import Barber
from HairClipper import HairClipper
from CurlingIron import CurlingIron
from ServiseType import ServiseType
import random
import math
import pickle


class Barbershop:
    def __init__(self, budget):
        if not str(budget).isdigit() or not int(budget) > 150:
            self._budget = 150
        else:
            self._budget = int(budget)
        self._registrations = []
        self._barbers = []
        self._hair_clipper_cost = 10
        self._curling_iron_cost = 15  # стоимость плойки
        self._barber_pay = 70
        self._chair_cost = 20
        self._mirror_cost = 30

    @property
    def budget(self):
        return self._budget

    def add_registration(self, name, day, time, service_type, hair_length, hair_type):
        if not all([
            day.isdigit() and int(day) in range(1, 8),
            time.isdigit() and int(time) in range(8, 20),
            service_type.isdigit() and int(service_type) in range(1, 4),
            hair_length.isdigit() and 0 < float(hair_length) < 100,
            hair_type.isdigit() and int(hair_type) in (1, 2)
        ]):
            raise ValueError("Неверные входные данные")
        if len(self._barbers) == 0:
            return "Вы не можете добавить записи клиентов пока нет ни одного работника "
        new_client = Client(name, day, time, service_type, hair_length, hair_type)
        index_to_insert = 0
        for i, client in enumerate(self._registrations):
            if client.day > new_client.day or (client.day == new_client.day and client.time > new_client.time):
                break
            index_to_insert = i + 1
        if len(self._registrations) > (len(self._barbers) - 1):
            return "Невозможно добавить запись на данный день и время так как все парикхмахеры будут заняты"
        self._registrations.insert(index_to_insert, new_client)
        service_type_name = ServiseType.types[new_client.service_type - 1]["name"]
        return f"Клиент {name} записан на день: {new_client.day}  время: {time} услуга: {service_type_name} "

    def barbers_not_empty(self):
        return bool(self._barbers)

    def delete_registration(self, index):
        if index.isdigit() and int(index) in range(1, len(self._registrations) + 1):
            name = self._registrations[int(index) - 1]
            self._registrations.pop(int(index) - 1)
            return f"Запись клиента {name} удалена "
        else:
            return "Неверный индекс"

    def print_all_registrations(self):
        response = "\nСписок всех записей:"
        i = 1
        for client in self._registrations:
            service_type_name = ServiseType.types[client.service_type - 1]["name"]
            response += f"\n{i}. Имя: {client.name} День: {client.day} Время: {client.time} Тип услуги: {service_type_name}"
            i += 1
        return response

    def find_available_barber(self):
        for index, barber in enumerate(self._barbers):
            if isinstance(barber, Barber) and barber.available:
                return index
        return None

    def _mirror_looking(self, service_name):
        rand_num = random.randint(0, 2)
        if rand_num == 0:
            self._budget += 10
            return f"\nКлиент посмотрел в зеркало и ему очень понравилась {service_name}\nКлиент оставил чаевые в размере 20"
        elif rand_num == 1:
            self._budget += 0
            return f"\nКлиент посмотрел в зеркало и ему  понравилась {service_name}\nКлиент оставил чаевые в размере 10"
        else:
            return f"\nКлиент посмотрел в зеркало и поблагодарил парикмахера за работу"

    def serve_one_client(self, client, id):
        response = f"\nУслугу выполняет парикмахер {self._barbers[id].name}"
        response += f"\nКлиент {client.name} сел на стул"
        if client.service_type == 1:
            response += self._barbers[id].make_haircut(client)
        elif client.service_type == 2:
            response += self._barbers[id].make_hair_styling(client)
        elif client.service_type == 3:
            response += "Проведена консультация по уходу за волосами"
        response += f"\nКлиент {client.name} встал со стула"
        service_cost = ServiseType.types[client.service_type - 1]["cost"]
        service_name = ServiseType.types[client.service_type - 1]["name"]
        service_cost = ServiseType.types[client.service_type - 1]["cost"]
        self._budget += service_cost
        response += self._mirror_looking(service_name)
        response += f"\nУслуга {service_name} оплачена клиентом {client.name} стоимость: {service_cost} \n"
        return response

    def perform_all_registered_services(self):
        response = "\nОтчёт о выполненных услугах"
        list_id = []
        for client in self._registrations:
            if isinstance(client, list):
                for each_client in client:
                    id = self.find_available_barber()
                    self._barbers[id].available = False
                    list_id.insert(id)
                    response += self.serve_one_client(each_client, id)
                for i in list_id:
                    self._barbers[i].available = True
                list_id = []
            else:
                response += self.serve_one_client(client, 0)
        self._registrations = []
        summary_pay = self._barber_pay * len(self._barbers)
        self._budget -= summary_pay
        response += f"\nРаботникам выплачены зарплаты. Суммарно {summary_pay}"
        return response

    def add_barber(self):
        if self._budget >= self._barber_pay:
            self._budget -= self._barber_pay
            new_barber = Barber(f"barber {self.barbers_count}")
            self._barbers.append(new_barber)

    def _add_instruments_for_barber(self, barber):
        new_hair_clipper = HairClipper()
        barber.add_instrument(new_hair_clipper)
        new_curling_iron = CurlingIron()
        barber.add_instrument(new_curling_iron)

    # закупка инструментов и найм работнииков
    def purchase(self):
        count = math.floor((self._budget - len(self._barbers)) / (
                self._barber_pay + self._curling_iron_cost + self._hair_clipper_cost + self._chair_cost + self._mirror_cost))
        self._budget -= count * (
                self._curling_iron_cost + self._hair_clipper_cost + self._chair_cost + self._mirror_cost)
        for i in range(count):
            barber_name = f"Barber {len(self._barbers)}"
            new_barber = Barber(barber_name)
            self._barbers.append(new_barber)
            self._add_instruments_for_barber(new_barber)
        return f"Нанято новых парикхмахеров  {len(self._barbers)} и закуплено необходимое оборудование.\nОставшийся бюджет {self._budget} "

    def save_state(self, file_name):
        with open(file_name, "wb") as f:
            pickle.dump(self.__dict__, f)

    def load_state(self, file_name):
        with open(file_name, "rb") as f:
            state = pickle.load(f)
            self.__dict__.update(state)

    @property
    def budget(self):
        return self._budget

    @property
    def registrations_count(self):
        return len(self._registrations)

    @property
    def barbers_count(self):
        return len(self._barbers)
