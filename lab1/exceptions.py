class BookingException(Exception):
    def __init__(self, message: str):
        self.__message = message

    def __str__(self) -> str:
        return self.__message


class VisitorNotFoundException(Exception):
    def __init__(self, visitor_passport_id: str):
        self.__message = f"Visitor with passport id '{visitor_passport_id}' doesn't exist"

    def __str__(self) -> str:
        return self.__message
