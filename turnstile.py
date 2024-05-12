from ticket import Ticket


class Turnstile:
    def __init__(self):
        pass

    def check(self, ticket: Ticket):
        try:
            if ticket is not None:
                return True
            else:
                raise ValueError("У пассажира нет билета!")
        except ValueError as e:
            print(e)
            return False

