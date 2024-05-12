class Schedule:
    def __init__(self, date, time):
         self.__date: str = date
         self.__time: str = time

    def get_time(self):
        return self.__time

    def get_date(self):
        return self.__date
