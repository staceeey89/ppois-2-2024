from enum import Enum
import exceptions


class Gender(Enum):
    MALE = "мужской"
    FEMALE = "женский"

    @classmethod
    def from_string(cls, gender_str: str):
        result = {"мужской": cls.MALE,
                "женский": cls.FEMALE}.get(gender_str)

        if result is None:
            raise exceptions.InvalidGenderValue("Вы ввели неверное значение пола пользователя!")

        return result
