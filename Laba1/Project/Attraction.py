import Queue
class Attraction:

    def __init__(self, name, capacity):
        self.name:str = name
        self.security_requirements = []
        self.capacity: int = capacity
        self.queue = Queue.Queue()


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def security_requirements(self):
        return self._security_requirements

    @security_requirements.setter
    def security_requirements(self, value):
        self._security_requirements = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value

    def ride_attraction(self, visitor):
        for requirement in self.security_requirements:
            if requirement.min_height > visitor.height:
                print(
                    f"Sorry, {visitor.name}, you cannot ride {self.name} because you do not meet the minimum height requirement.")
                return
            if requirement.max_weight < visitor.weight:
                print(
                    f"Sorry, {visitor.name}, you cannot ride {self.name} because you exceed the maximum weight limit.")
                return
            if requirement.min_age > visitor.age:
                print(
                    f"Sorry, {visitor.name}, you cannot ride {self.name} because you are too young.")
                return
        while self.queue.count_visitors_attract >= self.capacity:
            print(f"Capacity: {self.capacity}. Queue is full. Waiting...")
            self.queue.join_queue_attraction(self.capacity)
        print("It's your turn! Let's go riding the attraction!")

