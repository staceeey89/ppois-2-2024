class Person:
    def __init__(self, name: str, age: int, cunning: bool) -> None:
        self._name = name
        self._age = age
        self._cunning = cunning

    def get_name(self) -> str:
        return self._name

    def get_age(self) -> int:
        return self._age


