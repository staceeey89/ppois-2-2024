from car import Car
import sys
from io import StringIO
from human import Human
from adddel import AddDel
from typegearsseason import Gears
from carxceptions import StartCarError, CarDriveError, InvalidGearError, \
                           InvalidAgeError, CarNotInListError, CurrentCarUnavailableError
                           

class Driver(AddDel, Human):

    def __init__(self, name: str, surname: str, age: int=18, vehicle_fleet: set[Car]=set()):
        
        super().__init__(name, surname, age)
        self.__vehicle_fleet: set[Car] = vehicle_fleet
        self.__current_car: Car = None

    def __str__(self):

        return super().__str__()[:-1] + ", " + str({"Vehicle fleet": self.__vehicle_fleet,
                                                    "Current car": self.__current_car})
    
    def __hash__(self):
        return hash((self._name, self._surname, self._age))

    def __eq__(self, other):

        if not isinstance(other, Driver):
            raise TypeError("right operand should be object of class Driver")
    
        return hash(self) == hash(other)
    

    def set_vehicle_fleet(self, new_vehicles: set[Car]): self.__vehicle_fleet = new_vehicles
    def get_vehicle_fleet(self) -> set[Car]: return self.__vehicle_fleet
    def get_current_car(self) -> Car: return self.__current_car
    def get_car_state(self) -> dict: 

        try:
            if not self.__current_car: raise CurrentCarUnavailableError
            else: return self.__current_car.light_indicators
        except CurrentCarUnavailableError: 
            print("ERROR! You are not choosing current car for operation\n") 

    def repair_car(self): self.__current_car.repair()
    def oil_change(self): self.__current_car.change_oil()

    def add(self, car: Car): 
        
        if car not in self.__vehicle_fleet:
            self.__vehicle_fleet.add(car)
        else: print("Not added, because this car is already in list!\n")


    def __get_state(self, arg_list: list[str]=["Fuel", "Oil",
                                               "Engine", "Transmission",
                                               "Brakes", "Turn on"]) -> bool: 

        try:

            if not self.__current_car: raise CurrentCarUnavailableError
            else: 
                for arg in arg_list:
                    if not self.__current_car.light_indicators[arg]:
                        return False 

                return True

        except CurrentCarUnavailableError: 
            print("ERROR! You are not choosing current car for operation\n")    


    def change_gear(self, new_gear: Gears): 
        
        try:

            if not self.__current_car: raise CurrentCarUnavailableError
            else: self.__current_car.switch_gear(new_gear)

        except CurrentCarUnavailableError: 
            print("ERROR! You are not choosing current car for operation\n")


    def choose(self, car: Car): 
        
        try:

            if self.get_age() < 18: raise InvalidAgeError
            elif car in self.__vehicle_fleet:
                self.__current_car = car  
            else: raise CarNotInListError

        except InvalidAgeError: print("You are too young for this\n")
        except CarNotInListError: print("ERROR! This car is not in list!\n")
        
        
    def rem(self, car: Car):  

        if car in self.__vehicle_fleet: self.__vehicle_fleet.remove(car)
        else: print("Nothing to delete, because this car is not in list\n")
    

    def start_engine(self):

        try:

            if not self.__current_car: raise CurrentCarUnavailableError
            elif (self.__get_state(["Fuel", "Engine", "Oil", "Transmission"])) and \
                  not (self.__get_state(["Turn on"])): 
                
                self.__current_car.switch_engine()

            elif self.__get_state(["Turn on"]): print("Your engine is already turning on\n")
            else: raise StartCarError

        except StartCarError: print("ERROR! Your car is out of order\n")
        except CurrentCarUnavailableError: 
            print("ERROR! You are not choosing current car for operation\n")
        

    def stop_engine(self):

        try:

            if not self.__current_car: raise CurrentCarUnavailableError
            elif self.__get_state(["Turn on"]): self.__current_car.switch_engine()
            else: print("Your engine is already turning off\n")
        
        except CurrentCarUnavailableError:
            print("ERROR! You are not choosing current car for operation\n")


    def drive_forward(self):
        
        try:

            if not self.__current_car: raise CurrentCarUnavailableError
            elif self.__current_car.light_indicators["Gear"] in \
                 [Gears.N, Gears.R]: 
            
                raise InvalidGearError

            elif self.__get_state(["Fuel", "Engine", "Transmission", 
                               "Wheels", "Turn on", "Oil"]): 
                
                self.__current_car.increment_mileage()
                self.__current_car.decrease_fuel_level()
                self.__current_car.damage_engine()
                self.__current_car.damage_transmission()
                self.__current_car.damage_wheels()
                self.__current_car.oil_waste()

            else: raise CarDriveError

        except CurrentCarUnavailableError: 
            print("ERROR! You are not choosing current car for operation\n")

        except InvalidGearError: print("ERROR! Can't drive, because current gear is invalid\n")
        except CarDriveError: print("ERROR! Your car is out of order\n")


    def drive_back(self): 

        try:

            if not self.__current_car: raise CurrentCarUnavailableError
            elif self.__current_car.light_indicators["Gear"] in \
                 [Gears.R, None]:

                if self.__get_state(["Fuel", "Engine", "Transmission", 
                                   "Wheels", "Turn on", "Oil"]): 
                
                    self.__current_car.increment_mileage()
                    self.__current_car.decrease_fuel_level()
                    self.__current_car.damage_engine()
                    self.__current_car.damage_transmission()
                    self.__current_car.damage_wheels()
                    self.__current_car.oil_waste()

                else: raise CarDriveError

            else: raise InvalidGearError
        
        except CurrentCarUnavailableError: 
            print("ERROR! You are not choosing current car for operation\n")

        except InvalidGearError: print("ERROR! Can't drive, because current gear is invalid\n")
        except CarDriveError: print("ERROR! Your car is out of order\n")
        

    def drive_right(self):
        
        try:

            if not self.__current_car: raise CurrentCarUnavailableError
            elif self.__current_car.light_indicators["Gear"] in \
                 [Gears.N, Gears.R]: 
            
                raise InvalidGearError

            elif self.__get_state(): 

                self.__current_car.increment_mileage()
                self.__current_car.decrease_fuel_level()
                self.__current_car.damage_engine()
                self.__current_car.damage_transmission()
                self.__current_car.damage_wheels()
                self.__current_car.damage_brakes()
                self.__current_car.oil_waste()

            else: raise CarDriveError

        except CurrentCarUnavailableError: 
            print("ERROR! You are not choosing current car for operation\n")

        except InvalidGearError: print("ERROR! Can't drive, because current gear is invalid\n")
        except CarDriveError: print("ERROR! Your car is out of order\n")


    def drive_left(self): self.drive_right()


        

    
    
