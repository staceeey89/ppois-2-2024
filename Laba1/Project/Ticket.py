class Ticket:
    def __init__(self, attraction, cost, session_datetime, ticket_type, additional_info=None):
        self._attraction = attraction
        self._price = cost
        self.session_datetime = session_datetime
        self.ticket_type = ticket_type
        self.additional_info = additional_info

    @property
    def attraction(self):
        return self._attraction

    @attraction.setter
    def attraction(self, value):
        self._attraction = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value



