class InvalidPowerValue(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidResolutionValue(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidButtonException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidFilterHealthValue(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidNozzleValue(Exception):
    def __init__(self, message: str):
        super().__init__(message)