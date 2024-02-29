class Actor:
    def __init__(self, name="", age=15):
        self._name = str(name)
        self._age = int(age)

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age
