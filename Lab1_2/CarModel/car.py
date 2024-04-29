from random import randint
from engine import Engine
from wheels import Wheels
from transmission import Transmission
from typegearsseason import Gears
from brakes import Brakes
from detail import Detail

class Car:

    def __init__(self, engine: Engine, wheels: Wheels, transmission: Transmission, 
                 brakes: Brakes, car_name: str, creation_year: int=2024):
        
        self.__creation_year: int = creation_year if (1984 <= creation_year <= 2024) else 2024
        self.__name: str = car_name
        self.__engine: Engine = engine
        self.__wheels: Wheels = wheels
        self.__transmission: Transmission = transmission
        self.__brakes: Brakes = brakes
        self.__mileage: int = 10000 * (2024 - self.__creation_year)

    def __str__(self):
        
        return str({"Car name": self.__name, "Creation year": self.__creation_year, 
                    "Engine": (self.__engine.get_vendor(), self.__engine.get_creation_year()),
                    "Wheels": (self.__wheels.get_vendor(), self.__wheels.get_creation_year()),
                    "Brakes": (self.__brakes.get_vendor(), self.__brakes.get_creation_year()),
                    "Transmission": (self.__transmission.get_vendor(), self.__transmission.get_creation_year())})  

    @property
    def light_indicators(self) -> dict:    

        return {"Fuel": self.__engine.get_fuel_level(), 
                "max Fuel": self.__engine.get_max_fuel_level(),
                "Oil": self.__engine.is_oil(),
                "Engine": bool(self.__engine.get_state()), 
                "Wheels": bool(self.__wheels.get_state()),
                "Transmission": bool(self.__transmission.get_state()), 
                "Gear": self.__transmission.get_gear(),
                "Brakes": bool(self.__brakes.get_state()), 
                "Turn on": self.__engine.is_working(), 
                "Mileage": self.__mileage}
    
    def get_creation_year(self) -> int: return self.__creation_year
    def get_name(self) -> str: return self.__name
    def get_engine(self) -> Engine: return self.__engine
    def get_wheels(self) -> Wheels: return self.__wheels
    def get_transmission(self) -> Transmission: return self.__transmission
    def get_brakes(self) -> Brakes: return self.__brakes

    def damage_engine(self): self.__engine.damage()
    def damage_wheels(self): self.__wheels.damage()
    def damage_transmission(self): self.__transmission.damage()
    def damage_brakes(self): self.__brakes.damage()

    def increment_mileage(self): self.__mileage += 1
    def change_oil(self): self.__engine.set_oil(True)
    def decrease_fuel_level(self): self.__engine.fuel_waste()
    def switch_engine(self): self.__engine.change_working()
    def switch_gear(self, new_gear: Gears): self.__transmission.set_gear(new_gear)
    def refueling(self): self.__engine.maximize_fuel_level()

    def oil_waste(self): 
        if randint(1, 10) == 5: 
            self.__engine.set_oil(False)


    def repair(self):

        details: list[Detail] = [self.__engine, self.__wheels, 
                                 self.__transmission, self.__brakes]

        for detail in details:
            if detail.get_state() != 10: detail.restore()





    

