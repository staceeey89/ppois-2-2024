

class Instrument:
    def __init__(self, name: str):
        self.name = name
        self.status = True

    def clearing(self):
        if self.status:
            print("у вас чистый инструмент")
        else:
            self.status = True
            print("Вы почистили инструмент")
