import pickle
import threading
import time
from datetime import datetime
from json import JSONDecodeError
from types import NoneType
from typing import List

from cold_storage import ColdStorage
from fisherman import Fisherman, Experience
from market import Market
from net import Net
from ship import Ship
from util.serialization_util import Util


class FisheryProduction:
    def __init__(self, cold_storage: ColdStorage, market: Market) -> None:
        self.fishermen = []
        self.free_nets = []
        self.ships = []
        self.cold_storage = cold_storage
        self.market = market
        self.borrowed_ships: List[Ship] = []
        self.borrowed_fishermen: List[Fisherman] = []
        self.borrowed_nets: List[Net] = []

    def display_menu(self) -> None:
        print("Меню действий:")
        print("1. Организовать рыбалку")
        print("2. Закончить рыбалку и отправить рыбу на склад")
        print("3. Обработать рыбу")
        print("4. Заморозить рыбу")
        print("5. Перевести рыбу со склада на рынок")
        print("6. Добавить корабль")
        print("7. Добавить рыбака")
        print("8. Добавить сеть")
        print("9. Выйти")

    def fishery_operations(self) -> None:
        self.open_market()
        while True:
            self.display_menu()
            choice = input("Выберите действие: ")

            if choice == "1":
                self.organize_fishing()
            elif choice == "2":
                self.end_fishing_and_store_fish()
            elif choice == "3":
                self.process_fish()
            elif choice == "4":
                self.freeze_fish()
            elif choice == "5":
                self.transport_fish_to_market()
            elif choice == "6":
                self.add_ship()
            elif choice == "7":
                self.add_fisherman()
            elif choice == "8":
                self.add_net()
            elif choice == "9":
                print("Выход из программы.")
                self.finish_production()
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите действие из меню.")

    def organize_fishing(self) -> None:
        if self.fishermen and self.ships:
            self.display_ships()
            ship = self.choose_ship()
            self.display_fishermen()
            fishermen = self.choose_fishermen()
            self.display_nets()
            self.choose_nets(ship)
            ship.add_fishermen(fishermen)
            thread = threading.Thread(target=ship.start_fishing)
            thread.start()
        else:
            print("Нет рыбаков или кораблей для рыбалки.")

    def end_fishing_and_store_fish(self) -> None:
        if self.borrowed_ships:
            ship = self.borrowed_ships.pop()
            ship.fishing_event.set()
            "Ждем прибытия корабля"
            time.sleep(5)
            ship.set_fishing_event()
            self.return_fishermen(ship.fishermen)
            self.return_ship(ship)
            self.return_nets(ship)
            ship.transport_fish(self.cold_storage)
            print("Рыбаки, корабль и сети возвращены после рыбалки.")
        else:
            print("Рыбу на данный момент не вылавливают")

    def process_fish(self) -> None:
        self.cold_storage.process_fish()

    def freeze_fish(self) -> None:
        while True:
            try:
                print(f"Всего на складе {self.cold_storage.calculate_weight(is_for_selling=False)} кг рыбы")
                weight = int(input("Введите количество кг для заморозки: "))
                self.cold_storage.freeze_fish(weight)
                break
            except ValueError:
                print("Введите число")

    def transport_fish_to_market(self) -> None:
        while True:
            try:
                print(f"Всего на складе {self.cold_storage.calculate_weight(is_for_selling=True)} кг рыбы")
                limit = int(input("Введите максимальное количество кг: "))
                fish_to_market = self.cold_storage.sell_fish_to_market(limit)
                self.market.receive_fish_from_storage(self.cold_storage, fish_to_market)
                break
            except ValueError:
                print("Введите число")

    def add_ship(self) -> None:
        name = input("Введите название корабля: ")
        ship = Ship(name)
        self.ships.append(ship)

    def add_fisherman(self) -> None:
        experience_map = {
            "новичок": Experience.BEGINNER,
            "средний": Experience.INTERMEDIATE,
            "продвинутый": Experience.ADVANCED,
            "эксперт": Experience.EXPERT
        }

        while True:
            try:
                name = input("Введите имя рыбака: ")
                choice = input("Введите уровень опыта: Новичок, Средний, Продвинутый, Эксперт: ").lower()
                experience = experience_map[choice]
                fisherman = Fisherman(name, experience)
                self.fishermen.append(fisherman)
                break
            except KeyError:
                print("Ошибка: Повторите ввод")

    def add_net(self) -> None:
        while True:
            try:
                square = int(input("Введите площадь сети: "))
                net = Net(square)
                self.free_nets.append(net)
                break
            except ValueError:
                print("Введите число")

    def open_market(self) -> None:
        thread = threading.Thread(target=self.market.sell_fish)
        thread.start()

    def close_market(self) -> None:
        self.market.market_event.set()

    def finish_production(self) -> None:
        self.close_market()
        while self.borrowed_ships:
            self.end_fishing_and_store_fish()

    def display_ships(self) -> None:
        print("Выберите судно: ")
        for i, ship in enumerate(self.ships, 1):
            print(f"{i}. {str(ship)}")

    def display_fishermen(self) -> None:
        print("Выберите рыбаков: ")
        for i, fisherman in enumerate(self.fishermen, 1):
            print(f"{i}. {str(fisherman)}")

    def display_nets(self) -> None:
        print("Выберите сетки: ")
        for i, net in enumerate(self.free_nets, 1):
            print(f"{i}. {str(net)}")

    def choose_ship(self) -> Ship:
        while True:
            try:
                choice = input("Номер судна: ")
                ship = self.ships[int(choice) - 1]
                self.borrowed_ships.append(ship)
                self.ships.remove(ship)
                return ship
            except (IndexError, ValueError):
                print("Ошибка: Неверный выбор судна. Пожалуйста, введите корректный номер судна.")

    def choose_fishermen(self) -> List[Fisherman]:
        while True:
            try:
                choice = input("Выберите рыбаков: ")
                fishermen_list = choice.split()
                fishermen_numbers = [int(number) for number in fishermen_list]
                chosen_fishermen = [self.fishermen[i - 1] for i in fishermen_numbers]
                self.borrowed_fishermen.extend(chosen_fishermen)
                for fisherman in chosen_fishermen:
                    self.fishermen.remove(fisherman)
                return chosen_fishermen
            except (IndexError, ValueError):
                print("Ошибка: Неверный выбор рыбаков. Пожалуйста, введите корректные номера рыбаков.")

    def choose_nets(self, ship: Ship) -> None:
        while True:
            try:
                if self.free_nets:
                    choice = input("Номера сеток: ")
                    nets_list = choice.split()
                    nets_numbers = [int(number) for number in nets_list]
                    nets = [self.free_nets[i - 1] for i in nets_numbers]
                    for net in nets:
                        ship.add_net(net, is_casted=False)
                    for net in nets:
                        self.free_nets.remove(net)
                    for net in self.borrowed_nets:
                        ship.add_net(net, is_casted=True)
                    self.borrowed_nets.extend(nets)
                else:
                    for net in self.borrowed_nets:
                        ship.add_net(net, is_casted=True)
                break
            except (IndexError, ValueError):
                print("Ошибка: Неверный выбор сеток. Пожалуйста, введите корректные номера сеток.")

    def return_ship(self, ship) -> None:
        self.ships.append(ship)

    def return_fishermen(self, fishermen) -> None:
        for fisherman in fishermen:
            self.borrowed_fishermen.remove(fisherman)
            self.fishermen.append(fisherman)

    def return_nets(self, ship: Ship) -> None:
        for net in ship.taken_nets:
            try:
                self.borrowed_nets.remove(net)
                self.free_nets.append(net)
            except ValueError:
                pass
        ship.taken_nets = []
        ship.casted_nets = []

    def to_dict(self) -> dict:
        data = {
            'cold_storage': self.cold_storage.to_dict(),
            'market': self.market.to_dict(),
            'fishermen': [fisherman.to_dict() for fisherman in self.fishermen],
            'free_nets': [net.to_dict() for net in self.free_nets],
            'ships': [ship.to_dict() for ship in self.ships],
            'borrowed_ships': [ship.to_dict() for ship in self.borrowed_ships],
            'borrowed_fishermen': [fisherman.to_dict() for fisherman in self.borrowed_fishermen],
            'borrowed_nets': [net.to_dict() for net in self.borrowed_nets]
        }
        return data

    @staticmethod
    def create_object(data) -> 'FisheryProduction':
        cold_storage = Util.create_cold_storage(data['cold_storage'])
        market = Util.create_market(data['market'])
        fishermen = Util.create_fishermen(data['fishermen'])
        free_nets = Util.create_nets(data['free_nets'])
        ships = Util.create_ships(data['ships'])
        borrowed_ships = Util.create_borrowed_ships(data['borrowed_ships'])
        borrowed_fishermen = Util.create_borrowed_fishermen(data['borrowed_fishermen'])
        borrowed_nets = Util.create_borrowed_nets(data['borrowed_nets'])

        fishery_production = FisheryProduction(cold_storage, market)
        fishery_production.fishermen = fishermen
        fishery_production.free_nets = free_nets
        fishery_production.ships = ships
        fishery_production.borrowed_ships = borrowed_ships
        fishery_production.borrowed_fishermen = borrowed_fishermen
        fishery_production.borrowed_nets = borrowed_nets

        return fishery_production


if __name__ == "__main__":
    util = Util()
    while True:
        try:
            data1 = Util.load_state("fishery_production.json")
            fishery_production = FisheryProduction.create_object(data1)
        except JSONDecodeError:
            print("Файл не найден. Создается новый объект FisheryProduction.")
            market = Market("Рынок", [])
            cold_storage = ColdStorage("Хранилище", [], [], [])
            fishery_production = FisheryProduction(cold_storage, market)

        fishery_production.fishery_operations()
        util.save_state("fishery_production.json", fishery_production)
        choice = input("Хотите продолжить? (да/нет): ")
        if choice.lower() != "да":
            break
