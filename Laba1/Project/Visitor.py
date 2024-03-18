
class Visitor:
    def __init__(self, name: str, height:str):
        self.name = name
        self.height = height

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def buy_ticket(self, attraction, ticket):
        print(f"{self.name} bought a ticket for ${ticket.price} on {attraction.name}.")
        return ticket

    def choose_attraction(self, attractions):
        print("List of attractions:")
        for i, attraction in enumerate(attractions, start=1):
            print(f"{i}. {attraction.name}")

        attraction_choice = int(input("Enter the number of the attraction: "))
        if attraction_choice < 1 or attraction_choice > len(attractions):
            raise ValueError("Invalid attraction choice.")

        return attractions[attraction_choice-1]

    def wait_in_queue(self, attraction, queue):
        print(f"{self.name} is waiting in the queue for {attraction.name}.")
        queue.add_visitor(self)

    def watch_rules(self, attraction):
        print("Требования безопасности для данного аттракциона:")
        for i, rule in enumerate(attraction.security_requirements, start=1):
            print(f"{i}. {rule.rule}")
