class InvalidAgeValue(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidResolutionValue(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidGenderValue(Exception):
    def __init__(self, message: str):
        super().__init__(message)
