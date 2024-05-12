from dataclasses import dataclass


@dataclass
class User:
    user_id: int = -1
    name: str = ""
    surname: str = ""
    patronymic: str = ""
    account: str = ""
    address: str = ""
    mobile_number: str = ""
    landline_number: str = ""

    def __iter__(self):
        for field, value in self.__dict__.items():
            if field == "user_id":
                continue
            yield field, value
