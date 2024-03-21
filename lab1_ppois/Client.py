class Client:
    def __init__(self, name):
        self.name = name
        self.properties_interest = []

    def add_property_interest(self, property):
        self.properties_interest.append(property)

    def receive_document(self, document):
        print(f"Документ {document} получен клиентом {self.name}.")

    def __str__(self):
        return self.name