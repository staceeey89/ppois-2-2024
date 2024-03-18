class Person:
    def __init__(self, name, affiliation):
        self.__name = name
        self.__affiliation = affiliation

    def get_name(self):
        return self.__name

    def get_affiliation(self):
        return self.__affiliation

    def set_name(self, name):
        try:
            self.__name = name
        except ValueError:
            print("Имя должно быть строкой.")


    def set_affiliation(self, affiliation):
        try:
            self.__affiliation = affiliation
        except ValueError:
            print("Место работы должно быть строкой.")