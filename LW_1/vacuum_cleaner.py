import os
import time
from nozzle import Nozzle
from dust_container import DustContainer
from filter import Filter
from engine import Engine
from control_buttons import ControlButtons
from room import Room


class VacuumCleaner:
    def __init__(self, color: str, firm: str):
        self.color: str = color
        self.firm: str = firm
        self.nozzle = Nozzle()
        self.dust_container = DustContainer()
        self.filter = Filter()
        self.engine = Engine()
        self.control_buttons = ControlButtons()

    def put_on_nozzle(self, picked_nozzle: str):
        print(f"Надета насадка {picked_nozzle}")
        if picked_nozzle == "Turbo Brush":
            self.nozzle.turbo_brush = True
        elif picked_nozzle == "Slot Nozzle":
            self.nozzle.slot_nozzle = True
        elif picked_nozzle == "Round Nozzle":
            self.nozzle.round_nozzle = True
        elif picked_nozzle == "Laminate Nozzle":
            self.nozzle.laminate_nozzle = True
        elif picked_nozzle == "Corner Nozzle":
            self.nozzle.corner_nozzle = True
        else:
            print("Введенная насадка отсутсвует")

    def change_nozzle(self, new_nozzle: str):
        self.nozzle.turbo_brush = False
        self.nozzle.slot_nozzle = False
        self.nozzle.round_nozzle = False
        self.nozzle.laminate_nozzle = False
        self.nozzle.corner_nozzle = False
        self.put_on_nozzle(new_nozzle)

    def show_nozzle(self):
        print("У вас надета насадка: ", end='')
        if self.nozzle.turbo_brush:
            print("Turbo Brush")
        elif self.nozzle.slot_nozzle:
            print("Slot Nozzle")
        elif self.nozzle.round_nozzle:
            print("RoundNozzle")
        elif self.nozzle.laminate_nozzle:
            print("Laminate Nozzle")
        elif self.nozzle.corner_nozzle:
            print("Corner Nozzle")
        else:
            print("-")

    def clean_dust_container(self):
        self.dust_container.isFilled = False
        print("Контейнер для пыли очищен.")

    def check_dust_container(self):
        if self.dust_container.isFilled:
            print("Контейнер для пыли засорён")
        else:
            print("Контейнер для пыли чист")

    def show_power(self):
        print(f"Диапазон мощности на пылесосе от {self.engine.min_power} до {self.engine.max_power} Вт.")
        print(f"Текущая мощность {self.control_buttons.using_power} Вт.")

    def clean_room(self, dust_room: Room):
        dust_room.isClean = True
        self.dust_container.isFilled = True
        self.filter.usage_of_filter()
        self.engine.usage_of_engine()
        time_impl = 0.05*dust_room.square + 5/self.control_buttons.using_power
        percent = 0
        for i in range(11):
            print(f"Выполняется уборка: {percent}% ", end='')
            print(i * "█")
            time.sleep(time_impl)
            percent += 10
            os.system("clear")
        print("Помещение успешно убрано!")

    def technical_work(self):
        self.engine.renew_health()
        self.filter.renew_filter()
        self.clean_dust_container()
        print("Техническое обслуживание выполнено.")

    def start_vacuum(self, wishful_power: int):
        self.control_buttons.change_power(wishful_power)
        self.control_buttons.start_b = True
        print(f"Пылесос запущен.")

    def check_filter_health(self):
        print("До замены фильтра осталось чисток: " + str(self.filter.health))
