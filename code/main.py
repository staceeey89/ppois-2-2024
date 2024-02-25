from typing import List, Tuple
import pickle
from Turnstile import Turnstile
from Schedule import Schedule
from Station import Station
from Ticket import Ticket
from Person import Person
from Train import Train


def save_state(objects: List, filename: str) -> None:
    try:
        with open(filename, "wb") as f:
            pickle.dump(objects, f)
    except FileNotFoundError:
        print("The file could not be saved")


def load_state(filename: str) -> Tuple:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("The file could not be opened")
        return create_initial_state()


def create_initial_state() -> Tuple[Turnstile, Schedule, Ticket]:
    print("Creating initial state...")
    print("Before starting, input some data: ")
    turnstile: Turnstile = Turnstile()
    schedule: Schedule = Schedule()
    station_a: Station = Station(Station.StationName.STATION_A.value)
    station_b: Station = Station(Station.StationName.STATION_B.value)
    station_c: Station = Station(Station.StationName.STATION_C.value)
    station_service: Station = Station(Station.StationName.STATION_SERVICE.value)
    schedule.add_station(station_a)
    schedule.add_station(station_b)
    schedule.add_station(station_c)
    schedule.add_station(station_service)
    ticket_price: float = 0
    try:
        ticket_price: float = float(input("Enter ticket price: "))
    except ValueError:
        print("Invalid input. Default value 0")
    ticket: Ticket = Ticket(ticket_price)
    train_number: str = str(input("Enter train number: "))
    train: Train = Train(train_number, station_service)
    schedule.add_train(train)
    return turnstile, schedule, ticket


def station_selection() -> Station:
    print("Select a station")
    for i, station in enumerate(schedule.stations, 1):
        print(f"{i}. {station.station_name}")
    station_choice: str = input("Choose a station by entering its number or name: ")
    try:
        if len(schedule.stations) >= int(station_choice) > 0:
            station_index: int = int(station_choice) - 1
            chosen_station: Station = schedule.stations[station_index]
            print(f"You have chosen station: {chosen_station.station_name}")
            return chosen_station
        else:
            return schedule.stations[0]
    except ValueError:
        for station in schedule.stations:
            if station.station_name.lower() == station_choice.lower():
                chosen_station = station
                print(f"You have chosen station: {chosen_station.station_name}")
                return chosen_station
        else:
            print("Invalid choice. Please enter a valid station number or name.")
            return schedule.stations[0]


def create_person() -> Person:
    person_name: str = str(input("Enter name: "))
    person_money: float = 0
    try:
        person_money: float = float(input("Enter the amount of money the person will have: "))
    except ValueError:
        print("Invalid input. Default value is 0")
    return Person(person_name, person_money)


loaded_objects: [] = load_state("code/metro_state.pkl")
ticket: Ticket = None
schedule: Schedule = None
turnstile: Turnstile = None
for obj in loaded_objects:
    if isinstance(obj, Schedule):
        print("Stations: ")
        for i, station in enumerate(obj.stations, 1):
            print(f"{i}. {station.station_name}")
        print("Trains: ")
        for i, train in enumerate(obj.trains, 1):
            print(f"{i}. {train.number}")
        schedule = obj
    elif isinstance(obj, Ticket):
        print("Ticket price:", obj.price)
        ticket = obj
    elif isinstance(obj, Turnstile):
        print("Turnstile exist")
        turnstile = obj
    else:
        print("Unknown object type:", type(obj))

while True:
    print("~~~~Menu~~~~\n", "1. Show the number of people at the stations\n",
          "2. Add a person to the station\n",
          "3. To transport people\n",
          "4. exit")
    key: int = 4
    try:
        key: int = int(input())
    except ValueError:
        print("Invalid input")
    if key == 1:
        for i in range(len(schedule.stations)):
            print(i + 1, schedule.stations[i].station_name)
            print(schedule.stations[i].platform.get_people_count())
    if key == 2:
        person: Person = create_person()
        person.buy_ticket(ticket)
        chosen_station = station_selection()
        person.enter_platform(chosen_station.platform, turnstile)
    if key == 3:
        print("Choose which train to send")
        schedule.move_train()
    if key == 4:
        objects_to_save = [turnstile, schedule, ticket]
        save_state(objects_to_save, "code/metro_state.pkl")
        break
