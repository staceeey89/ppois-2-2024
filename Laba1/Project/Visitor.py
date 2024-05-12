from Ticket import Ticket

class Visitor:
    def __init__(self, name=None, height=None, weight=None, age=None):
        self.name: str = name
        self.height: float = height
        self.weight: float = weight
        self.age: int = age
        self.tickets = []

    def get_visitor_info(self):
        while True:
            name = input("Enter visitor's name: ")
            if name:
                self.name = name
                break
            else:
                print("Name cannot be empty!")
        while True:
            try:
                height = float(input("Enter visitor's height (in cm): "))
                if 70 <= height <= 250:
                    self.height = height
                    break
                else:
                    print("Height must be a correct number!")
            except ValueError:
                print("Invalid input! Please enter a number for height.")
        while True:
            try:
                weight = float(input("Enter visitor's weight (in kg): "))
                if 15 <= weight <= 250:
                    self.weight = weight
                    break
                else:
                    print("Weight must be a correct number!")
            except ValueError:
                print("Invalid input! Please enter a number for weight.")
        while True:
            try:
                age = int(input("Enter visitor's age: "))
                if 1 <= age <= 90:
                    self.age = age
                    break
                else:
                    print("Age must be a correct integer!")
            except ValueError:
                print("Invalid input! Please enter an integer for age.")
        print("Visitor Information:")
        print(f"Name: {self.name}")
        print(f"Height: {self.height} cm")
        print(f"Weight: {self.weight} kg")
        print(f"Age: {self.age}")

    def buy_ticket(self, park, queue):
        queue.join_queue_ticket()
        print("List of attractions:")
        for i, attraction in enumerate(park.attractions, start=1):
            print(f"{i}. {attraction.name}")

        attraction_choice = int(input("Enter the number of the attraction: "))
        if attraction_choice < 1 or attraction_choice > len(park.attractions):
            raise ValueError("Invalid attraction choice.")
        selected_attraction = park.attractions[attraction_choice - 1]

        num_tickets = int(input("Enter the number of tickets: "))
        if num_tickets <= 0:
            raise ValueError("Number of tickets should be greater than 0.")

        for _ in range(num_tickets):
            ticket = Ticket(selected_attraction)
            self.tickets.append(ticket)
            print(f"{self.name} bought a ticket {ticket.number} for {selected_attraction.name}.")
    def choose_attraction(self, park):
        print("List of attractions:")
        for i, attraction in enumerate(park.attractions, start=1):
            print(f"{i}. {attraction.name}")

        attraction_choice = int(input("Enter the number of the attraction: "))
        if attraction_choice < 1 or attraction_choice > len(park.attractions):
            raise ValueError("Invalid attraction choice.")
        selected_attraction = park.attractions[attraction_choice - 1]
        try:
            if selected_attraction not in [ticket.attraction for ticket in self.tickets]:
                raise Exception("You don't have a ticket for this attraction. Please, buy ticket first")
        except Exception as e:
            print(e)
        else:
            for ticket in self.tickets:
                if ticket.attraction == selected_attraction:
                    self.tickets.remove(ticket)
                    break
            self.visit_attraction(selected_attraction)

    def visit_attraction(self, attraction):
        attraction.ride_attraction(self)


    def watch_rules(self, park):
        print("List of attractions:")
        for i, attraction in enumerate(park.attractions, start=1):
            print(f"{i}. {attraction.name}")

        attraction_choice = int(input("Enter the number of the attraction: "))
        if attraction_choice < 1 or attraction_choice > len(park.attractions):
            raise ValueError("Invalid attraction choice.")
        selected_attraction = park.attractions[attraction_choice - 1]
        print("Security requirements for this attraction:")
        for i, rule in enumerate(selected_attraction.security_requirements, start=1):
            print(f"{i}. {rule.rule}  Min Height: {rule.min_height}, Max Weight: {rule.max_weight} Min Age: {rule.min_age}")

    def watch_tickets(self):
        print("My purchased tickets :")
        tickets_by_attraction = {}  # Словарь для хранения количества билетов на каждый аттракцион
        for ticket in self.tickets:
            attraction_name = ticket.attraction.name
            if attraction_name in tickets_by_attraction:
                tickets_by_attraction[attraction_name] += 1
            else:
                tickets_by_attraction[attraction_name] = 1

        # Выводим список билетов с указанием количества на каждый аттракцион
        for i, (attraction_name, count) in enumerate(tickets_by_attraction.items(), start=1):
            print(f"{i}. {attraction_name} - {count} ticket/s")