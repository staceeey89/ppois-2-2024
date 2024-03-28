from typing import List, Tuple
import pickle
from Person import Person
from Railway import Railway
from Schedule import ScheduleItem
from Schedule import Schedule
from Station import Station
from Ticket import Ticket
from Train import Train
from Train import Wagon
from datetime import datetime


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


def create_initial_state() -> Tuple[Train, Schedule, Railway]:
    print("Creating initial state...")

    train_number: int = 1
    try:
        train_number: int = int(input("Enter the train number: "))
    except ValueError:
        print("Invalid input. Default value is 1")
    train: Train = Train(train_number)
    wagon_1: Wagon = Wagon(1)
    wagon_2: Wagon = Wagon(2)
    wagon_3: Wagon = Wagon(3)
    train.add_wagon(wagon_1)
    train.add_wagon(wagon_2)
    train.add_wagon(wagon_3)
    train.locomotive.start_engine()

    schedule: Schedule = Schedule()

    railway_number: int = 1
    try:
        railway_number: int = int(input("Enter the railway number: "))
    except ValueError:
        print("Invalid input. Default value is 1")
    railway: Railway = Railway(railway_number)
    first_station: Station = Station("First Station")
    railway.add_station(first_station)
    train.choise_railway(railway)
    return train, schedule, railway


loaded_objects: [] = load_state("data.pkl")
train: Train = loaded_objects[0]
schedule: Schedule = loaded_objects[1]
railway: Railway = loaded_objects[2]

while True:
    print("___Menu___\n",
          "1. Add a station to the railway\n",
          "2. Add a person to the station\n",
          "3. Show information about stations\n",
          "4. Go ahead to 1 station\n",
          "5. Pick up all the people at the selected station to the selected wagon\n",
          "6. Drop off all passengers\n",
          "7. Аdd an item to the schedule\n",
          "8. Show the schedule\n",
          "9. exit")
    key: int = 9
    try:
        key: int = int(input())
    except ValueError:
        print("Invalid input")

    if key == 1:

        station_name: str = "Default Station"
        try:
            station_name: str = str(input("Enter the station name: "))
        except ValueError:
            print("Invalid input. Default value is Default Station")

        station: Station = Station(station_name)
        railway.add_station(station)

    if key == 2:

        person_name: str = "Default Person"
        try:
            person_name: str = str(input("Enter the person name: "))
        except ValueError:
            print("Invalid input. Default value is Default Person")

        person_balance: int = 100
        try:
            person_balance: int = int(input("Enter the person balance: "))
        except ValueError:
            print("Invalid input. Default value is 100")

        person: Person = Person(person_name, person_balance)
        ticket: Ticket = Ticket(10)
        person.buy_ticket(ticket)

        while True:
            try:
                number_of_station: int = int(input("Enter the station number: "))
            except ValueError:
                print("Invalid input.")
                continue
            if number_of_station >= len(railway.stations) or number_of_station < 0:
                print("Invalid input.")
                continue
            person.select_station(railway.stations[number_of_station-1])
            break

    if key == 3:
        for i in range(len(railway.stations)):
            print(i + 1, railway.stations[i].name)
            print(railway.stations[i].get_persons())
            print(railway.stations[i].get_trains())

    if key == 4:
        train.move_forward()

    if key == 5:
        number_of_wagon = 0
        try:
            number_of_wagon: int = int(input("Enter the number of wagon: "))
        except ValueError:
            print("Invalid input. Default value is 0")
        train.board_all_persons(number_of_wagon)

    if key == 6:
        train.leave_all_persons()

    if key == 7:
        number_of_station: int = 1
        while True:
            try:
                number_of_station: int = int(input("Enter the station number: "))
            except ValueError:
                print("Invalid input.")
                continue
            if number_of_station >= len(railway.stations) or number_of_station < 0:
                print("Invalid input.")
                continue
            break
        while True:
            arrival_time_str = input("Enter arrival time (format: YYYY-MM-DD HH:MM): ")
            try:
                arrival_time = datetime.strptime(arrival_time_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid arrival time format. Schedule item not added.")
                continue
            item = ScheduleItem(train, railway.stations[number_of_station - 1], arrival_time)
            schedule.add_item(item)
            break

    if key == 8:
        schedule.show_schedule()

    if key == 9:
        objects_to_save = [train, schedule, railway]
        save_state(objects_to_save, "data.pkl")
        break
