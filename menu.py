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
    bool_is_started: bool = 0
    global chosen_passenger, choose_platf
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

            passengers[chosen_passenger].station = stations[chosen_station]
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
                choose_platf = int(input())
                if choose_platf == 0 or choose_platf == 1:
                    break
            passengers[chosen_passenger].choose_a_platform(stations[chosen_station].get_platforms()[choose_platf])
            stations[chosen_station].get_platforms()[choose_platf].add_passenger(passengers[chosen_passenger])
            print("Платформа выбрана!")
            continue
        elif choice == 9:
            if schedule.get_stations_list()[chosen_station].get_platforms()[choose_platf].train is not None:
                passengers[chosen_passenger].board(stations[chosen_station].get_platforms()[passengers[chosen_passenger].platform.number].train)
                print("Пассажир в поезде!")
            else:
                print("Поезда нет")
            continue

        elif choice == 10:
            schedule.get_stations_list()[chosen_station].get_platforms()[choose_platf].train.get_passengers()[chosen_passenger].disembark(schedule.get_stations_list()[chosen_station].get_platforms()[choose_platf].train)
            print("Пассажир покинул поезд!")
            continue
        elif choice == 11:
            if bool_is_started:
                print("Метро уже работает")
                continue
            if len(stations) < 2:
                print(f"Недостаточно станций для движения ({len(stations)})")
                continue

            bool_is_started = True
            schedule.fill_depots()
            print("Поезда готовы к запуску!")
            continue
        elif choice == 12:
            schedule.next_phase()
            if passengers[chosen_passenger].platform.number == 0 and chosen_station + 1 != len(stations):
                chosen_station += 1
            elif passengers[chosen_passenger].platform.number == 1 and chosen_station - 1 != -1:
                chosen_station -= 1
            print("Поезда уже на следующей станции!")
        elif choice == 13:
            train: Train = Train()
            schedule.add_train(train)
            print("Поезд добавлен в список!")
        elif choice == 14:
            schedule.run_a_train()
            print("Поезда запущены в первые станции!")
        elif choice == 15:
            schedule.print_info()
            if passengers[chosen_passenger].station is not None:
                print(f"Текущая станция {passengers[chosen_passenger].station.number}")
            else:
                print(f"Пассажир еще в поезде")
            continue
        elif choice == -1:
            break


if __name__ == "__main__":
    main()
