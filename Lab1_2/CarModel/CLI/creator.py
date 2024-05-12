from colorama import Fore

from driver import Driver
from car import Car
from typegearsseason import TransmissionType, Gears, Season
from wheels import Wheels
from brakes import Brakes
from transmission import Transmission
from engine import Engine

class Creator():

    __default_engine = Engine(90, "Volta")
    __default_wheels = Wheels(Season.summer, "Cordiant", 2018)
    __default_transmission = Transmission(TransmissionType.automatic, "Aisin", 2020)
    __default_brakes = Brakes("Advics", 2023)
    __default_car = Car(__default_engine, __default_wheels, 
                      __default_transmission, __default_brakes, 
                      "Lada Vesta")

    __new_engine = Engine(100, "MAN Diesel")
    __new_summer_wheels = Wheels(Season.summer, "Michelin")
    __new_automatic_transmission = Transmission(TransmissionType.automatic, "Eaton")
    __new_brakes = Brakes("ATE")
    __new_car = Car(__new_engine, __new_summer_wheels,
                  __new_automatic_transmission, __new_brakes, 
                  "Nissan Interstar")

    __old_engine = Engine(70, "Deere & Company", 2016)
    __old_winter_wheels = Wheels(Season.winter, "Bridgestone", 2016)
    __old_mechanical_transmission = Transmission(TransmissionType.mechanical, "Jatco")
    __old_brakes = Brakes("Ferodo")
    __old_car = Car(__old_engine, __old_winter_wheels, 
                  __old_mechanical_transmission, __old_brakes, 
                  "Chevrolet N200", 2008)

    __standart_driver = Driver("Nikita", "Sloboda", 19)

    @classmethod
    def get_car_kit(cls) -> set[Car]: 
        return {cls.__default_car, cls.__new_car, cls.__old_car}
    
    @classmethod
    def get_standart_driver(cls) -> Driver: return cls.__standart_driver

    def input_int(message: str, min: int=0, max: float=float("inf")) -> int:

        while True:
            try:

                integer = int(input(Fore.LIGHTYELLOW_EX + message))

                if integer > max or integer < min: raise ValueError
                break

            except ValueError: 
                print(Fore.LIGHTMAGENTA_EX + f"Only integer number({min}-{max}). Try again")

        return integer  

    def create_engine() -> Engine:

        engine_volume = Creator.input_int("Enter engine volume: ")
        engine_vendor = input("Enter vendor of engine: ")
        engine_creation_year = Creator.input_int("Enter engine creation year: ", 2014, 2024)
        fuel_level = Creator.input_int("Enter fuel level: ", max=engine_volume)
        oil = bool(input("Is there oil in engine?: "))

        return Engine(engine_volume, engine_vendor, engine_creation_year, 
                      fuel_level, oil)
    
    def create_wheels() -> Wheels:
        
        season = input("Enter wheels season(summer OR winter): ")
        match season:

            case "summer" | 1: wheels_season = Season.summer
            case "winter" | 2: wheels_season = Season.winter
            case _: 
                
                wheels_season = Season.summer
                print(Fore.LIGHTMAGENTA_EX + "This season is not exist. Set default season: summer")
        
        wheels_vendor = input(Fore.LIGHTYELLOW_EX + "Enter vendor of wheels: ")
        wheels_creation_year = Creator.input_int("Enter wheels creation year: ", 2014, 2024)

        return Wheels(wheels_season, wheels_vendor, wheels_creation_year)

    def create_transmission() -> Transmission:

        type = input("Enter transmission type(automatic OR mechanical): ")
        match type:

            case "automatic" | 1: transmission_type = TransmissionType.automatic
            case "mechanical" | 2: transmission_type = TransmissionType.mechanical
            case _:

                transmission_type = TransmissionType.mechanical
                print(Fore.LIGHTMAGENTA_EX + "This type is not exist. Set default type: mechanical")

        transmission_vendor = input(Fore.LIGHTYELLOW_EX + "Enter vendor of transmission: ")
        transmission_creation_year = Creator.input_int("Enter transmisssion creation year: ", 2014, 2024)

        return Transmission(transmission_type, transmission_vendor,
                            transmission_creation_year)

    def create_brakes() -> Brakes:

        brakes_vendor = input("Enter vendor of brakes: ")
        brakes_creation_year = Creator.input_int("Enter brakes creation year: ", 2014, 2024)

        return Brakes(brakes_vendor, brakes_creation_year)