
class Queue:
    def __init__(self):
        self.visitors = []

    @property
    def visitors(self):
        return self._visitors

    @visitors.setter
    def visitors(self, value):
        self._visitors = value

    def display_queue(self):
        print("Queue:")
        for i, visitor in enumerate(self.visitors, start=1):
            print(f"{i}. {visitor.name}")

    def add_visitor(self, visitor, attraction):
        if len(self.visitors) >= attraction.capacity:
            raise Exception("Queue is full. Cannot add more visitors.")
        self.visitors.append(visitor)

    def remove_visitor(self):
        if self.visitors:
            return self.visitors.pop(0)
        else:
            raise Exception("Queue is empty.")