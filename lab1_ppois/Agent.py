class Agent:
    def __init__(self, name):
        self.name = name
        self.properties_managed = []

    def add_property_managed(self, property):
        self.properties_managed.append(property)

    def receive_commission(self, amount):
        print(f"Агент {self.name} получил сумму за объект в размере {amount}.")

    def __str__(self):
        return self.name
