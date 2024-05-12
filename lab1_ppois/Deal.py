class Deal:
    def __init__(self, property, client, agent, documents):
        self.property = property
        self.client = client
        self.agent = agent
        self.documents = documents

    def __str__(self):
        return f" для объекта недвижимости {self.property} с {self.client} обслуживаемая {self.agent}"



