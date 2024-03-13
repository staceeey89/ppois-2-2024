from plot import Plot
from plant import Plant


class RecreationArea(Plot):
    def __init__(self, type_: str, square: int):
        super().__init__(type_, square)
        self.decorations = []
        print("зона отдыха успешно создана!")

    def __check(self, name: str):
        if self.decorations.__sizeof__() == 0:
            return True
        for decoration in self.decorations:
            if name == decoration:
                print("такое украшение уже имеется")
                return False
        return True

    def decoration(self, instruments: []):
        print("как вы хотите украсить свою зону отдыха")
        print("1. цветы")
        print("2. украшения")
        a = input()
        while not (a == '2' or a == '1'):
            print("повторите попытку")
            a = input()
        if a == "1":
            name = input("какое растение вы хотите посадить: ")
            plant = Plant(name)
            self.planting_a_plant(plant, instruments)
        if a == "2":
            name = input("какое украшение хотите разместить: ")
            if self.__check(name):
                self.decorations.append(name)
                print("вы успешно поместили украшение")

    def print_list_of_decorations(self):
        if len(self.decorations) == 0:
            print("у вас нет украшений")
            return
        for decoration in self.decorations:
            print(decoration)
