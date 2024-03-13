from plant import Plant
from soil import Soil
from irrigation_system import IrrigationSystem


class Plot:
    def __init__(self, type_: str, square: int):
        self.soil = Soil(type_)
        self.square = square
        self.plants = []

    def planting_a_plant(self, plant: Plant, instruments: []):
        if len(instruments) == 0:
            print("у вас нет инструментов")
            return
        what = input("какой вам нужен инструмент: ")
        for instrument in instruments:
            if what == instrument.name:
                if instrument.status:
                    instrument.status = False
                    plant.planting()
                    self.plants.append(plant)
                else:
                    print("надо почистить инструмент")
            else:
                print("у вас нет инструментов")

    def print_list_of_the_plants(self):
        if len(self.plants) == 0:
            print("у вас нет растений на участке")
        for index, plant in enumerate(self.plants):
            print("индекс: ", index, "название растения: ", plant.name, "посажено: ", plant.is_planted, "ухожено: ",
                  plant.well_groomed, "полито: ", plant.is_watering)

    def watering_my_plants(self, irrigation_system: IrrigationSystem):
        if len(self.plants) == 0:
            print("у вас пока нет растений")
            return
        print("вы хотите удобрять одно растение(1) или все(2)")
        a = input()

        while not (a == '2' or a == '1'):
            print("повторите попытку")
            a = input()
        if a == '2':
            if irrigation_system.turned_on:
                for plant in self.plants:
                    if not plant.is_watering:
                        plant.watering()
                        self.soil.watering()
        if a == '1':
            name = input("какое растение вы хотите полить")
            if irrigation_system.turned_on:
                for plant in self.plants:
                    if plant.name == name:
                        plant.watering()
                        print("вы полили растение " + name)

    def take_care_of_plant(self, instruments: []):
        what = input("какой вам нужен инструмент: ")
        for instrument in instruments:
            if what == instrument.name:
                if instrument.status:
                    instrument.status = False
                    for plant in self.plants:
                        plant.take_care_of()
                else:
                    print("надо почистить инструмент")

    def fertilize_plants(self, irrigation_system: IrrigationSystem):
        if len(self.plants) == 0:
            print("у вас пока нет растений")
            return
        print("вы хотите удобрять одно растение(1) или все(2)")
        a = input()

        while not (a == '2' or a == '1'):
            print("повторите попытку")
            a = input()


        if a == '2':
            if irrigation_system.turned_on:
                if irrigation_system.dunged:
                    print("вам нужно заправить систему полива удобрением")
                else:
                    for plant in self.plants:
                        if not plant.is_watering:
                            plant.fertilizing()
                            self.soil.fertilizing()
                    print("вы удобрили свои растения")
        if a == '1':
            name = input("какое растение вы хотите полить")
            if irrigation_system.turned_on:
                if irrigation_system.dunged:
                    print("вам нужно заправить систему полива удобрением")
                else:
                    for plant in self.plants:
                        if plant.name == name:
                            plant.fertilizing()
                            self.soil.fertilizing()
                            print("вы удобрили растение " + name)
