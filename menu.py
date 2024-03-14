from typing import List

from passenger import Passenger
from train import Train
from schedule import Schedule
from platf import Platform
from ticket import Ticket
from depot import Depot
from turnstile import Turnstile
from station import Station

def main():
    print("\t\tДобро пожаловать в модель метро!\nМеню выбора операций:")
    schedule = Schedule()
    while True:
        print("1. Создать пассажира\t2. Создать станцию метро\t3. Создать билет метро"
              "\n4. Продать пассажиру билет\t5. Пройти турникет пассажиру\t6. Выбрать станцию для посадки"
              "\n7. Выбрать платформу\t8 Сесть в поезд\t9 Выйти из поезда\t10 Выяснить актуальную станцию метро"
              "\n11. Выяснить время до ближайшего поезда\t12. Отправить поезда на ветке на следующую станцию"
              "\n13. Создать поезд\t-1. Выход")
        choice: int = int(input())
        if choice == 1:
            print("Имя:")
            name = input()
            print("Кол-во денег:")
            cash = int(input())
            passenger = Passenger(name, cash)
            print("Пассажир создан!")
            continue
        elif choice == 2:
            print("Номер станции:")
            num = int(input())
            station = Station(num)
            schedule.add_station(station)
        elif choice == 3:
            ticket = Ticket()

if __name__ == "__main__":
    main()
