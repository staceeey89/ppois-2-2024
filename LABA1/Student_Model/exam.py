from .schedule import Schedule


class Exam:
    def __init__(self, name, date, time):
        self.__name: str = name
        self.__schedule: Schedule = Schedule(date, time)

    def get_name(self) -> str:
        return self.__name

    def get_schedule(self):
        return self.__schedule

