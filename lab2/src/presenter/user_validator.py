import re

from src.model.user import User


class UserValidator:
    name_pattern = re.compile(r"[А-Я][а-я]+")
    surname_pattern = name_pattern
    patronymic_pattern = name_pattern
    account_pattern = re.compile(r"\d{6}")
    address_pattern = re.compile(
        r"((ул\.)|(пр-кт)|(пер\.)|(пл\.)|(пр.))( [А-Я]\.)?( [А-Я]\.)?( [А-Я][а-я]+)+, [1-9][0-9]*(/[а-я])?"
    )
    mobile_pattern = re.compile(r"\d{9}")
    landline_pattern = re.compile(r"\d{9,11}")

    def validate_user(self, user: User) -> User:
        self.validate_user_name(user.name)
        self.validate_user_surname(user.surname)
        self.validate_user_patronymic(user.patronymic)
        self.validate_user_account(user.account)
        self.validate_user_address(user.address)
        self.validate_user_mobile(user.mobile_number)
        self.validate_user_landline(user.landline_number)
        return user

    def validate_user_name(self, name: str) -> None:
        if not self.name_pattern.match(name):
            raise ValueError("Invalid name")

    def validate_user_surname(self, surname: str) -> None:
        if not self.surname_pattern.match(surname):
            raise ValueError("Invalid surname")

    def validate_user_patronymic(self, patronymic: str) -> None:
        if not self.patronymic_pattern.match(patronymic):
            raise ValueError("Invalid patronymic")

    def validate_user_account(self, account: str) -> None:
        if not self.account_pattern.match(account):
            raise ValueError("Invalid account")

    def validate_user_address(self, address: str) -> None:
        if not self.address_pattern.match(address):
            raise ValueError("Invalid address")

    def validate_user_mobile(self, mobile_number: str) -> None:
        if not self.mobile_pattern.match(mobile_number):
            raise ValueError("Invalid mobile number")

    def validate_user_landline(self, landline_number: str) -> None:
        if not self.landline_pattern.match(landline_number):
            raise ValueError("Invalid landline number")
