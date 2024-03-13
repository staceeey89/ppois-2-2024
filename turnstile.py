from ticket import Ticket


class Turnstile:
    def __init__(self):
        pass

    def check(self, ticket: Ticket):
        try:
            if ticket is not None:
                return True
            else:
                Exception("Buy a ticket!")
        except Exception as text:
            print(text)
            return False
