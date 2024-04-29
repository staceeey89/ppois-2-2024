from time import sleep
from colorama import Fore

from CLI.cli import CLI
from CLI.creator import Creator
from CLI.help import print_help
from typegearsseason import TransmissionType, Gears, Season
from wheels import Wheels
from brakes import Brakes
from transmission import Transmission
from engine import Engine
from car import Car
from driver import Driver
from gasstation import GasStation

class Main():

    __drivers: set[Driver] = set()
    __current_driver: Driver = None

    @classmethod
    def __add_standart_driver(cls) -> None: 

        driver: Driver = Creator.get_standart_driver()
        if driver not in cls.__drivers:

            cls.__drivers.add(driver)
            print(Fore.LIGHTGREEN_EX + "SUCCESS! Standart driver was added in drivers\n")
        
        else: print(Fore.RED + "ERROR! Standart driver is already in drivers\n")
    
    @classmethod
    def __create_driver(cls) -> None:

        name: str = input(Fore.LIGHTYELLOW_EX + "Enter driver name: ")
        surname: str = input("Enter driver surname: ")
        age: int = Creator.input_int("Enter driver age: ", 1, 120)
        print("\n")
        driver: Driver = Driver(name, surname, age)

        if driver not in cls.__drivers:
            cls.__drivers.add(driver)
            print(Fore.LIGHTGREEN_EX + "SUCCESS! Driver was added in drivers\n")

        else: print(Fore.RED + "ERROR! This driver is already in drivers\n")

    @classmethod
    def __change_driver(cls) -> None: 

        name: str = input(Fore.LIGHTYELLOW_EX + "Enter driver name: ")
        surname: str = input("Enter driver surname: ")
        age: int = Creator.input_int("Enter driver age: ", 1, 120)
        print("\n")
        driver: Driver = Driver(name, surname, age)

        for element in cls.__drivers:
            if driver == element:

                cls.__current_driver = element
                print(Fore.LIGHTGREEN_EX + "SUCCESS! Driver has been changed\n")
                break

        else: print(Fore.RED + "ERROR! This driver is not in drivers\n")
        
    @classmethod
    def __add_standart_cars(cls) -> None:

        if not cls.__current_driver:
            print(Fore.RED + "ERROR! Current driver is None\n")
            return

        cars: set[Car] = Creator.get_car_kit()
    
        if not cars.issubset(cls.__current_driver.get_vehicle_fleet()):

            for car in cars: cls.__current_driver.add(car)

            print(Fore.LIGHTGREEN_EX + "SUCCESS! Standart car-kit was added in vehicles\n")

        else: print(Fore.RED + "ERROR! This cars is already in vehicles\n")

    @classmethod
    def __create_car(cls) -> None: 

        if not cls.__current_driver:
            print(Fore.RED + "ERROR! Current driver is None\n")
            return

        engine: Engine = Creator.create_engine()
        print("\nEngine was created\n")
        wheels: Wheels = Creator.create_wheels()
        print("\nWheels was created\n")
        transmission: Transmission = Creator.create_transmission()
        print("\nTransmission was created\n")
        brakes: Brakes = Creator.create_brakes()
        print("\nBrakes was created\n")

        car_name: str = input("Enter car name: ")
        car_creation_year: int = Creator.input_int("Enter car creation year: ", 1984, 2024)
        car: Car = Car(engine, wheels, transmission, brakes, 
                       car_name, car_creation_year)
        
        cls.__current_driver.add(car)
        print(Fore.LIGHTGREEN_EX + "\nSUCCESS! Car was added in vehicles\n")

    @classmethod
    def __change_car(cls) -> None: 

        if not cls.__current_driver:
            print(Fore.RED + "ERROR! Current driver is None\n")
            return

        name: str = input(Fore.LIGHTYELLOW_EX + "Enter car name: ")
        print("\n")

        for car in cls.__current_driver.get_vehicle_fleet():
            if name == car.get_name():

                cls.__current_driver.choose(car)
                print(Fore.LIGHTGREEN_EX + "SUCCESS! Car has been changed\n")
                return
            
        print(Fore.RED + "ERROR! This car is not in vehicle fleet\n")
        
    @classmethod
    def __rem_car(cls) -> None: 

        if not cls.__current_driver:
            print(Fore.RED + "ERROR! Current driver is None\n")
            return

        name: str = input(Fore.LIGHTYELLOW_EX + "Enter car name: ")
        print("\n")

        for car in cls.__current_driver.get_vehicle_fleet():
            if name == car.get_name():

                cls.__current_driver.rem(car)
                print(Fore.LIGHTGREEN_EX + "SUCCESS! Car has been removed\n")
                break

        print(Fore.RED + "ERROR! This car is not in vehicle fleet\n")

    @classmethod
    def __change_gear(cls) -> None: 

        if cls.__current_driver.get_current_car().get_transmission().get_type() == \
           TransmissionType.automatic:
            
            print(Fore.MAGENTA + "You dont need switch gear, " + 
                  "because your transmission is automatic")
            return

        gears: set[Gears] = [Gears.N, Gears.R, Gears.G1, Gears.G2, Gears.G3, Gears.G4]

        CLI.print_gears()
        gear: int = Creator.input_int("Enter gear: ", max=5)
        print("\n")
        cls.__current_driver.change_gear(gear)
        print(Fore.LIGHTGREEN_EX + "SUCCESS! Gear was changed")

    @classmethod 
    def __drive_car_forward(cls) -> None: 
        cls.__current_driver.drive_forward()
        print(Fore.LIGHTGREEN_EX + "SUCCESS! Your car driving forward\n")

    @classmethod 
    def __drive_car_back(cls) -> None: 
        cls.__current_driver.drive_back()
        print(Fore.LIGHTGREEN_EX + "SUCCESS! Your car driving back\n")

    @classmethod 
    def __drive_car_right(cls) -> None: 
        cls.__current_driver.drive_right()
        print(Fore.LIGHTGREEN_EX + "SUCCESS! Your car driving right\n")

    @classmethod 
    def __drive_car_left(cls) -> None: 
        cls.__current_driver.drive_left()
        print(Fore.LIGHTGREEN_EX + "SUCCESS! Your car driving left\n")

    @classmethod
    def __print_car_state(cls) -> None:
        print(Fore.LIGHTWHITE_EX + f"{cls.__current_driver.get_car_state()}\n")

    @classmethod
    def __drive_car(cls) -> None:

        if not cls.__current_driver:
            print(Fore.RED + "ERROR! Current driver is None\n")
            return
        
        if not cls.__current_driver.get_current_car():
            print(Fore.RED + "ERROR! Current car is None\n")
            return
        
        command: int = 1
        drive_menu: list[function] = [cls.__current_driver.stop_engine, cls.__current_driver.start_engine,
                                      cls.__change_gear, cls.__drive_car_forward, 
                                      cls.__drive_car_back, cls.__drive_car_right,
                                      cls.__drive_car_left, cls.__print_car_state]
        
        while command:

            sleep(1)
            CLI.print_drive_menu()
            command = Creator.input_int("Enter your command: ", max=7)

            drive_menu[command]()

    @classmethod
    def __gasstation_queue_add(cls) -> None:
        
        name = input(Fore.LIGHTYELLOW_EX + "Enter car name: ")

        for car in cls.__current_driver.get_vehicle_fleet():
            if name == car.get_name():

                GasStation.add(car)
                print(Fore.LIGHTGREEN_EX + "SUCCESS! Car has been added in queue")
                return

        print(Fore.RED + "ERROR! This car is not in vehicle fleet\n")

    @classmethod
    def __gasstation_queue_rem(cls) -> None:
        
        name: str = input(Fore.LIGHTYELLOW_EX + "Enter car name: ")

        for car in cls.__current_driver.get_vehicle_fleet():
            if name == car.get_name():

                GasStation.rem(car)
                print(Fore.LIGHTGREEN_EX + "SUCCESS! Car has been removed from queue")
                return

        print(Fore.RED + "ERROR! This car is not in queue\n")
    
    @classmethod
    def __gasstation_queue_add_vehicles(cls) -> None:

        if not cls.__current_driver.get_vehicle_fleet().issubset(GasStation.get_queue()):

            GasStation.set_queue(cls.__current_driver.get_vehicle_fleet())
            print(Fore.LIGHTGREEN_EX + "SUCCESS! Car has been added in queue")

        else: print(Fore.RED + "ERROR! This cars is already in queue\n")

    @classmethod
    def __refueling(cls) -> None: 

        if GasStation.get_queue():

            cls.__current_driver.set_vehicle_fleet(set(GasStation.gen_refueling_cars()))
            print(Fore.LIGHTGREEN_EX + "SUCCESS! Cars has been refueled\n")

        else: print(Fore.RED + "ERROR! Queue is empty\n")

    @classmethod
    def __repair_curr_car(cls) -> None:

        cls.__current_driver.repair_car()
        print(Fore.LIGHTGREEN_EX + "SUCCESS! Your current car has been repaired")

    @classmethod
    def __curr_car_oil_change(cls) -> None:

        cls.__current_driver.oil_change()
        print(Fore.LIGHTGREEN_EX + "SUCCESS! Oil in your current car has been changed")

    @classmethod
    def __car_service(cls) -> None:

        if not cls.__current_driver:
            print(Fore.RED + "ERROR! Current driver is None")
            return

        command: int = 1
        service_menu: list[function] = [CLI.exit_from_service, cls.__gasstation_queue_add, cls.__gasstation_queue_rem,
                                        cls.__gasstation_queue_add_vehicles, cls.__refueling,
                                        cls.__repair_curr_car, cls.__curr_car_oil_change, 
                                        cls.__print_car_state]
        
        while command:

            sleep(1)
            CLI.print_service_menu()
            command =  Creator.input_int("Enter your command: ", max=7)
            service_menu[command]()

    @classmethod
    def __print_driver_info(cls) -> None: 

        if not cls.__current_driver:
            print(Fore.RED + "ERROR! Current driver is None")
            return

        print(Fore.WHITE + "Name: " + cls.__current_driver.get_name())
        print("Surname: " + cls.__current_driver.get_surname())
        print(f"Age: {cls.__current_driver.get_age()} \n")

        print(Fore.LIGHTYELLOW_EX + "\nVehicle Fleet:")

        for car in cls.__current_driver.get_vehicle_fleet():

            if car == cls.__current_driver.get_current_car():
                print(Fore.LIGHTYELLOW_EX + f"{car}\n")
            else: print(Fore.WHITE + f"{car}\n")

        sleep(2)

    @classmethod
    def __print_drivers(cls) -> None: 
        
        print(Fore.LIGHTYELLOW_EX + "Drivers list:\n")

        for driver in cls.__drivers:
            print("Name: " + driver.get_name())
            print("Surname: " + driver.get_surname())
            print(f"Age: {driver.get_age()} \n")

        sleep(2)

    @classmethod
    def command_input(cls) -> None:

        menu: list[function] = [exit, cls.__add_standart_driver, cls.__create_driver, 
                                cls.__change_driver, cls.__add_standart_cars, 
                                cls.__create_car, cls.__change_car, cls.__rem_car,
                                cls.__drive_car, cls.__car_service,
                                cls.__print_driver_info, cls.__print_drivers, print_help]
        
        command: int = Creator.input_int("Enter your command: ", max=12)       

        menu[command]()

if __name__ == "__main__":

    while True:
        
        sleep(1)
        CLI.print_menu()
        Main.command_input()



        















