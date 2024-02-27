def _get_day_of_week(number):
    if number == 1:
        return "Понедельник"
    elif number == 2:
        return "Вторник"
    elif number == 3:
        return "Среда"
    elif number == 4:
        return "Четверг"
    elif number == 5:
        return "Пятница"
    elif number == 6:
        return "Суббота"
    elif number == 7:
        return "Воскресенье"
    else:
        return "Неверный день недели"


class Client:
    def __init__(self, name, day, time, service_type, hair_length, hair_type):
        self._name = name
        self._day = _get_day_of_week(int(day))
        self._time = time
        self._service_type = int(service_type)
        self._hair_length = float(hair_length)
        if hair_type == "1":
            self._hair_type = "тонкие"
        else:
            self._hair_type = "плотные"

    @property
    def name(self):
        return self._name

    @property
    def day(self):
        return self._day

    @property
    def time(self):
        return self._time

    @property
    def service_type(self):
        return self._service_type

    @property
    def hair_length(self):
        return self._hair_length

    @property
    def hair_type(self):
        return self._hair_type
