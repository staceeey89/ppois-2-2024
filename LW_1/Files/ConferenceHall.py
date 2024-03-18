class ConferenceHall:
    def __init__(self, name, capacity):
        self.__name = name
        self.__capacity = capacity
        self.__bookings = []

    def get_name(self):
        return self.__name

    def get_capacity(self):
        return self.__capacity

    def get_bookings(self):
        return self.__bookings

    def set_name(self, name):
        try:
            self.__name = name
        except ValueError:
            print("Имя должно быть строкой.")

    def set_capacity(self, capacity):
        try:
            self.__capacity = capacity
        except ValueError:
            print("Вместимость должна быть положительным целым числом.")

    def add_booking(self, booking):
        try:
            self.__bookings.append(booking)
            print(f"Забронировано: {booking}")
        except ValueError:
            print("Детали брони должны быть строкой.")

    def cancel_booking(self, booking):
        if booking in self.__bookings:
            self.__bookings.remove(booking)
            print(f"Бронь отменена: {booking}")
        else:
            print(f"Бронь '{booking}' не найдена.")
