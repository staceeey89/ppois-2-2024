from Ticket import Ticket


class Person:
    def __init__(self, name: str, balance: int):
        self.name: str = name
        self.balance: int = balance
        if balance < 0:
            self.balance = 100
            print(f"The balance should not be negative. The balance is set at 100")
        self.ticket: Ticket = None
        self.station = None
        self.train = None

    def buy_ticket(self, ticket: Ticket) -> None:
        if self.ticket:
            print(f"{self.name} already has a ticket")
            return
        if ticket.purchased:
            print("This is someone else's ticket")
            return
        if self.balance >= ticket.price:
            self.balance -= ticket.price
            self.ticket = ticket
            ticket.purchased = True
            print(f"{self.name} bought a ticket")
        else:
            print("Not enough money")

    def select_station(self, station) -> None:
        self.station = station
        station.persons.append(self)
        print(f"{self.name} chose the station {station.name}.")

