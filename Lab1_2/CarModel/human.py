class Human:

    def __init__(self, name: str, surname: str, age: int=18):

        self._name: str = name
        self._surname: str = surname
        self._age: int = age if (1 <= age <= 120) else 18

    def get_name(self) -> str: return self._name
    def get_surname(self) -> str: return self._surname
    def get_age(self) -> str: return self._age 
    def set_name(self, new_name): self._name = new_name
    def set_surname(self, new_surname): self._surname = new_surname
    def set_age(self, new_age): 

        if (1 <= new_age <= 120):
            self._age = new_age
        else: print("Nothing changed, because this age is invalid")
