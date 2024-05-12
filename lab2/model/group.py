import uuid


class Group:
    def __init__(self, id: uuid.UUID, number: int):
        self.id = id
        self.number = number

    def __str__(self):
        return f'{self.id}, Group: {self.number}'
