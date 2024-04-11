from abc import ABC, abstractmethod
from typing import List, Dict
import sys

class Vehicle(ABC):
    @abstractmethod
    def prepare_for_battle(self):
        pass

    @abstractmethod
    def move_and_maneuver(self):
        pass

    @abstractmethod
    def fire_and_shoot(self):
        pass

    @abstractmethod
    def repair_and_maintenance(self):
        pass

    @abstractmethod
    def participate_in_military_training(self):
        pass

    @abstractmethod
    def engage_in_military_conflicts(self):
        pass

class CrewMember:
    def __init__(self, name: str, is_ready: bool):
        self.name = name
        self.is_ready = is_ready

class Equipment:
    def __init__(self, name: str, is_functional: bool):
        self.name = name
        self.is_functional = is_functional

class Fuel:
    def __init__(self, type: str, amount: int):
        self.type = type
        self.amount = amount

class Tank(Vehicle):
    def __init__(self, name: str, crew: List[CrewMember], equipment: List[Equipment], fuel: Fuel, number: int):
        self.name = name
        self.crew = crew
        self.equipment = equipment
        self.fuel = fuel
        self.number = number
        self.is_destroyed = False

    def prepare_for_battle(self):
        if not self.is_destroyed:
            print(f"Tank {self.name} is preparing for battle.")

    def move_and_maneuver(self):
        if not self.is_destroyed:
            print(f"Tank {self.name} is moving and maneuvering.")

    def fire_and_shoot(self):
        if not self.is_destroyed:
            print(f"Tank {self.name} is firing and shooting.")

    def repair_and_maintenance(self):
        if not self.is_destroyed:
            print(f"Tank {self.name} is being repaired and maintained.")

    def participate_in_military_training(self):
        if not self.is_destroyed:
            print(f"Tank {self.name} is participating in military training.")

    def engage_in_military_conflicts(self):
        if not self.is_destroyed:
            print(f"Tank {self.name} is engaging in military conflicts.")

    def destroy(self):
        self.is_destroyed = True
        print(f"Tank {self.name} has been destroyed.")

def create_tank(tanks: Dict[int, Tank]):
    number = len(tanks) + 1
    crew = [CrewMember("John", True), CrewMember("Jane", True)]
    equipment = [Equipment("Machine Gun", True), Equipment("Rocket Launcher", True)]
    fuel = Fuel("Diesel", 100)
    tank = Tank(f"T-34 No.{number}", crew, equipment, fuel, number)
    tanks[number] = tank
    print(f"Created tank T-34 No.{number}")
    return number

def destroy_tank(tanks: Dict[int, Tank], number: int):
    if number in tanks:
        tank = tanks[number]
        if not tank.is_destroyed:
            tank.destroy()
        else:
            print(f"Tank No.{number} has already been destroyed.")
    else:
        print(f"Tank No.{number} does not exist.")

def select_tank(tanks: Dict[int, Tank]):
    available_tanks = {number: tank for number, tank in tanks.items() if not tank.is_destroyed}
    if not available_tanks:
        print("No tanks available to select.")
        return None

    print("Available tanks:")
    for number in available_tanks:
        print(f"- {number}")
    selected_number = int(input("Enter tank number to select: "))
    if selected_number in available_tanks:
        print(f"Selected tank No.{selected_number}")
        return selected_number
    else:
        print(f"Tank No.{selected_number} does not exist or is destroyed.")
        return None

def change_tank_attribute(tanks: Dict[int, Tank], current_tank_number: int):
    if current_tank_number is None:
        print("No tank selected. Please select a tank or create a new one.")
        return

    tank = tanks[current_tank_number]
    print(f"Current tank name: {tank.name}")
    new_name = input("Enter new tank name: ")
    tank.name = new_name
    print(f"Tank name changed to: {tank.name}")

def list_tanks(tanks: Dict[int, Tank]):
    if not tanks:
        print("No tanks available.")
    else:
        print("List of tanks:")
        for number, tank in tanks.items():
            status = "Destroyed" if tank.is_destroyed else "Available"
            print(f"Tank No.{number}: {tank.name} ({status})")

def perform_action(tanks: Dict[int, Tank], current_tank_number: int, action: str):
    if current_tank_number is None:
        print("No tank selected. Please select a tank or create a new one.")
        return

    tank = tanks.get(current_tank_number)
    if tank is None:
        print("Tank does not exist.")
        return

    if tank.is_destroyed:
        print("Cannot perform action. The tank is destroyed.")
        return

    if action == 'prepare_for_battle':
        tank.prepare_for_battle()
    elif action == 'move_and_maneuver':
        tank.move_and_maneuver()
    elif action == 'fire_and_shoot':
        tank.fire_and_shoot()
    elif action == 'repair_and_maintenance':
        tank.repair_and_maintenance()
    elif action == 'participate_in_military_training':
        tank.participate_in_military_training()
    elif action == 'engage_in_military_conflicts':
        tank.engage_in_military_conflicts()
def main():
    tanks: Dict[int, Tank] = {}
    current_tank_number = None

    operations = {
        'create': lambda: create_tank(tanks),
        'destroy': lambda: destroy_tank(tanks, current_tank_number) if current_tank_number is not None else print("No tank selected"),
        'select': lambda: select_tank(tanks),
        'change': lambda: change_tank_attribute(tanks, current_tank_number) if current_tank_number is not None else print("No tank selected"),
        'list': lambda: list_tanks(tanks),
        'prepare': lambda: perform_action(tanks, current_tank_number, 'prepare_for_battle'),
        'move': lambda: perform_action(tanks, current_tank_number, 'move_and_maneuver'),
        'fire': lambda: perform_action(tanks, current_tank_number, 'fire_and_shoot'),
        'repair': lambda: perform_action(tanks, current_tank_number, 'repair_and_maintenance'),
        'train': lambda: perform_action(tanks, current_tank_number, 'participate_in_military_training'),
        'conflict': lambda: perform_action(tanks, current_tank_number, 'engage_in_military_conflicts'),
        'exit': lambda: sys.exit(0),  # Exit the program
    }

    while True:
        print("\nAvailable operations:")
        for operation in operations:
            print(f"- {operation}")
        operation = input("Enter operation: ")
        if operation in operations:
            if operation == 'select':
                current_tank_number = operations[operation]()
            else:
                operations[operation]()
        else:
            print("Invalid operation. Please try again.")



if __name__ == "__main__":
    main()