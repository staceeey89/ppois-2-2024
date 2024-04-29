class StartCarError(Exception):
    pass
    
class CarDriveError(Exception):
    pass

class SwitchAutomaticTransmissionError(Exception):
    pass

class CarNotInListError(ValueError):
    pass

class InvalidGearError(ValueError):
    pass

class InvalidAgeError(ValueError):
    pass

class CurrentCarUnavailableError(ValueError):
    pass