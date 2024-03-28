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
    passengers: List[Passenger] = []
    trains: List[Train] = []
    bool_is_started: bool = 0
    global chosen_passenger
    chosen_passenger = -1
    global chosen_station
    chosen_station = -1
    depot_1 = Depot()
    depot_2 = Depot()
    stations: List[Station] = []
    print("\t\tДобро пожаловать в модель метро!\nМеню выбора операций:")
    schedule = Schedule()
    schedule.add_depot(depot_1)
    schedule.add_depot(depot_2)
    ticket = Ticket()
    turnstile = Turnstile()

    while True:
        print("1. Создать пассажира\t2. Создать станцию метро\t3. Назначить цену проезда"
              "\n4. Выбрать пассажира\t5. Выбрать станцию\t6. Купить билет \t7. Пройти турникет "
              "\n8. Выбрать платформу\t9. Сесть в поезд\t10. Выйти из поезда"
              "\n11. Запустить метро \t12. Отправить поезда на следующие станции"
              "\n13. Добавить поезд\t14. Запустить поезда из депо на первые станции"
              "\n15 Вывести информацию о следующем поезде"
              "\n\t-1. Выход")
        choice: int = int(input())
        if choice == 1:
            print("Введите имя:")
            name = input()
            print("Кол-во денег:")
            cash = int(input())
            passenger = Passenger(name, cash)
            passengers.append(passenger)
            print("Пассажир создан!")
            continue
        elif choice == 2:
            print("Введите номер станции метро")
            number = int(input())
            platform_1 = Platform(0)
            platform_2 = Platform(1)
            station: Station = Station(number)
            station.add_platform(platform_1)
            station.add_platform(platform_2)
            station.turnstile = turnstile
            station.ticket = ticket
            stations.append(station)
            schedule.add_station(station)
            print("Станция создана!")
            continue
        elif choice == 3:
            print("Введите цену:")
            num = int(input())
            ticket.cost = num
            print("Цена задана!")
            continue
        elif choice == 4:
            i = 0
            for passenger in passengers:
                print(f"{passenger.name} index:{i}")
                i += 1
            while True:
                print("\nВыберите индекс пассажира:")
                chosen_passenger_check = int(input())
                if chosen_passenger_check <= i:
                    chosen_passenger = chosen_passenger_check
                    break
                else:
                    print("Такого пассажира нет.")
            print("Пассажир выбран!")
            continue
        elif choice == 5:
            i = 0
            for station in stations:
                print(f"{station.number} index:{i}")
                i += 1
            while True:
                print("\nВыберите индекс станции:")
                chosen_station_check = int(input())
                if chosen_station_check <= i:
                    chosen_station = chosen_station_check
                    break
                else:
                    print("Такой станции нет.")
            print("Станция выбрана!")
            continue
        elif choice == 6:
            try:
                stations[chosen_station].sell_a_ticket(passengers[chosen_passenger])
                print("Билет куплен!")
            except ValueError as e:
                print(e)
        elif choice == 7:
            passengers[chosen_passenger].cross_a_turnstile(stations[chosen_station].turnstile)
            print("Турникет пройден!")
        elif choice == 8:
            while True:
                print("Введите номер платформы: 0 или 1")
                choose_platf = bool(input())
                if choose_platf == 0 or choose_platf == 1:
                    break
            passengers[chosen_passenger].choose_a_platform(stations[chosen_station].get_platforms()[choose_platf])
            print("Платформа выбрана!")
            continue
        elif choice == 9:
            passengers[chosen_passenger].board(passengers[chosen_passenger].platform.train)
            print("Пассажир в поезде!")
            continue

        elif choice == 10:
            passengers[chosen_passenger].disembark(passengers[chosen_passenger].platform.train)
            print("Пассажир покинул поезд!")
            continue
        elif choice == 11:
            if bool_is_started:
                print("Метро уже работает")
                continue
            if len(stations) < 2:
                print(f"Недостаточно станций для движения ({len(stations)})")
                continue
            if len(trains) < 2:
                print(f"Недостаточно поездов для движения ({len(stations)})")
                continue

            bool_is_started = True
            for train in trains:
                schedule.add_train(train)
            schedule.fill_depots()
            schedule.run_a_train()
            print("Поезда уже на первых станциях!")
            continue
        elif choice == 12:
            schedule.next_phase()
            print("Поезда уже на следующей станции!")
        elif choice == 13:
            train: Train = Train()
            trains.append(train)
            print("Поезд добавлен в список!")
        elif choice == 14:
            schedule.run_a_train()
            print("Поезда запущены в первые станции!")
        elif choice == 15:
            schedule.print_info()
            print(f"Текущая станция {passengers[chosen_passenger].station}")
        elif choice == -1:
            break


if __name__ == "__main__":
    main()
