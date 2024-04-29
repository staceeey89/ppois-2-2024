from colorama import Fore
from time import sleep

doc_str = '''
This programm simulates driving a car and it's maintenance.
Command list:
|0| Exit - immediately close the programm.

|1| Add standart driver - adds standart driver(Nikita Sloboda 19) in the drivers list, if 
this driver already exists in this list: nothing to changes.

|2| Create driver and add it - starts creating driver process, then add created driver in drivers list,
if this driver already exists in this list: nothing to changes.
    Process description: 
    input 1: Any string (driver name);
    input 2: Any string (driver surname);
    input 3: Any positive integer number: to 120 (driver age). If this age will be lower than 18,
    he can't drive a car, but can have vehicle fleet;

|3| Change current driver - starts the process of changing the current driver.
    Process description: 
    input 1: Any string (driver name);
    input 2: Any string (driver surname);
    input 3: Any positive integer number: to 120 (driver age);
    NOTE: This driver should be in drivers list, otherwise: nothing to changes.

|4| Add standart car-kit to current driver - adds standart car-kit to current driver's vehicle fleet, if 
this cars already exists in vehicle fleet or current driver will be None: nothing to changes.
    Standart car-kit description:
    default car: Lada Vesta, 2024;
        -Engine: Volta, 2024, tank volume: 90, empty;
        -Wheels: Cordiant, 2018, summer;
        -Transmission: Aisin, 2020, automatic;
        -Brakes: Advics, 2023;
    
    new car: Nissan Interstar, 2024;
        -Engine: MAN Diesel, 2024, tank volume: 100, empty;
        -Wheels: Michelin, 2024, summer;
        -Transmission: Eaton, 2024, automatic;
        -Brakes: ATE, 2024;

    old car: Chevrolet N200, 2008;
        -Engine: Deere & Company, 2016, tank volume: 70, empty;
        -Wheels: Bridgestone, 2016, winter;
        -Transmission: Jatco, 2024, mechanical;
        -Brakes: Ferodo, 2024;

|5| Create car and add it to current driver - starts creating car process, then add created car 
to current driver's vehicle fleet, if this car already exists in vehicle fleet or current driver 
will be None: nothing to changes.
    Process description: 
    input 1: Any positive integer number (engine tank volume);
    input 2: Any string (engine vendor);
    input 3: Any positive integer number: from 2014 to 2024 (engine creation year);
    input 4: Any positive integer number: to tank volume (engine fuel level);
    input 5: Boolean value: 0(empty string) or 1(any not empty string)  (oil presentance);
    input 6: Enum value: summer or winter (wheels season), if value will be invalid, set default
    value: summer;
    input 7: Any string (wheels vendor);
    input 8: Any positive integer number: from 2014 to 2024 (wheels creation year);
    input 9: Any positive integer number: from 2014 to 2024 (engine creation year);
    input 10: Enum value: automatic or mechanical (transmission type), if value will be invalid, set default
    value: mechanical;
    input 11: Any string (transmission vendor);
    input 12: Any positive integer number: from 2014 to 2024 (transmission creation year);
    input 13: Any string (brakes vendor);
    input 14: Any positive integer number: from 2014 to 2024 (brakes creation year);
    input 15: Any string (car name);
    input 16: Any positive integer number: from 1984 to 2024 (car creation year);

|6| Change current car - starts the process of changing the current car, if current driver will be None:
nothing to changes.
    Process description: 
    input 1: Any string (car name);
    NOTE: This car should be in current driver's vehicle fleet, otherwise: nothing to changes.

|7| Remove car from car-list in current driver- starts removing car process, if current driver will be None:
nothing to changes.
    Process description: 
    input 1: Any string (car name);
    NOTE: This car should be in current driver's vehicle fleet, otherwise: nothing to changes.

|8| Drive current car - starts car driving mod, if current driver will be None: nothing will happen.
    Driving mod commands:
    |0| Stop driving and engine - exit from driving mod and stops current car engine.
    |1| Start engine - starts current car engine.
    |2| Change gear - starts the procees of changing current gear.
        Process description:
        input 1: Any positive integer number: to 5 (gear);
        NOTE: If transmission type of current car will be automatic, this process don't starts;
    |3| Drive forward - current car has been driving forward. 
    |4| Drive back - current car has been driving back. 
    |5| Drive right - current car has been driving right. 
    |6| Drive left - current car has been driving left. 
    |7| Car state - write car state in dictionary form.
        
|9| Current car service - starts car service mod, if current driver will be None: nothing will happen.
    Service mod commands:
    |0| Exit from service - exit from service mod.
    |1| Add car to gasstation-queue - starts the process of adding car to gasstation-queue.
        Process description: 
        input 1: Any string (car name);
        NOTE: This car should be in current driver's vehicle fleet, otherwise: nothing to changes;
    |2| Remove car from gasstation-queue - starts the process of removing car from gasstation-queue.
        Process description: 
        input 1: Any string (car name);
        NOTE: This car should be in gasstation-queue, otherwise: nothing to changes;
    |3| Add all vehicle fleet to gasstation-queue - adds current driver's vehicle fleet to 
    gasstation-queue.
    |4| Refueling all cars in gasstation-queue.
    |5| Repair current car.
    |6| Change oil in current car.
    |7| Car state - write car state in dictionary form.
    
|10| Info about current driver - prints info about current driver (name, surname, vehicle fleet).
|11| Drivers list - prints drivers list with personal information.
|12| Help.
'''

def print_help() -> None: 

    global doc_str 
    print(Fore.WHITE + doc_str)
    sleep(4)