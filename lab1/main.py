from hotel import *
import pickle


def main():
    with open('resources/save.pkl', 'rb') as f:
        hotel: Hotel = pickle.load(f)
    while True:
        print("1 - Add room")
        print("2 - Show available rooms")
        print("3 - Show all rooms")
        print("4 - Add worker")
        print("5 - Show unemployed workers")
        print("6 - Show all workers")
        print("7 - Fire off worker")
        print("8 - Book room")
        print("9 - Pay off for room")
        print("10 - Ask for service")
        print("11 - Ask for restaurant service")
        print("12 - Show uncompleted services: ")
        print("13 - Finish service: ")
        print("14 - Show all visitors: ")
        print("15 - Show all bookings: ")
        choice = input("Choice: ")
        # os.system('cls' if os.name == 'nt' else 'clear')
        if choice == '1':
            room_number = input("Input number of room: ")
            type_of_room = input("Input type of room: ")
            hotel.add_room(room_number, type_of_room)
        elif choice == '2':
            hotel.show_available_rooms()
        elif choice == '3':
            hotel.show_all_rooms()
        elif choice == '4':
            try:
                name = input("Enter name of worker: ")
                age = int(input("Enter age of the worker: "))
                passport_id = input("Enter worker passport id: ")
                hotel.add_worker(name, age, passport_id)
            except ValueError:
                print("Age must be an integer")
        elif choice == '5':
            hotel.show_unemployed_workers()
        elif choice == '6':
            hotel.show_all_workers()
        elif choice == '7':
            worker_passport_id = input("Enter worker passport id: ")
            hotel.fire_off_worker(worker_passport_id)
        elif choice == '8':
            try:
                name = input("Enter name of visitor: ")
                age = int(input("Enter age of the visitor: "))
                passport_id = input("Enter visitor passport id: ")
                room_number = input("Enter number of room: ")
                number_of_days = int(input("Enter for how long (in days): "))
                hotel.book_room(name, age, passport_id, room_number, number_of_days)
            except ValueError:
                print("Age and number of days must be an integer")
        elif choice == '9':
            visitor_passport_id = input("Input visitor passport id: ")
            hotel.pay_off(visitor_passport_id)
        elif choice == '10':
            worker_passport_id = input("Enter worker passport id: ")
            visitor_passport_id = input("Enter visitor passport id: ")
            service_type = input("Enter type of service: ")
            hotel.ask_for_service(worker_passport_id, visitor_passport_id, service_type)
        elif choice == '11':
            worker_passport_id = input("Enter worker passport id: ")
            visitor_passport_id = input("Enter visitor passport id: ")
            dishes: list[Dishes] = []
            dish = input("Enter name of dish or stop to end order: ")
            while dish != "stop":
                try:
                    dishes.append(Dishes[dish])
                    dish = input("Enter name of dish or stop to end order: ")
                except KeyError:
                    print("No such dish")
                    dish = input("Enter name of dish or stop to end order: ")
            if dishes:
                hotel.ask_for_restaurant_service(worker_passport_id, visitor_passport_id, dishes)
            else:
                print("You must order something")
        elif choice == '12':
            hotel.show_uncompleted_services()
        elif choice == '13':
            worker_passport_id = input("Enter worker passport id: ")
            hotel.finish_service(worker_passport_id)
        elif choice == '14':
            hotel.show_all_visitors()
        elif choice == '15':
            hotel.show_all_bookings()
        else:
            break

    with open('resources/save.pkl', 'wb') as f:
        pickle.dump(hotel, f)


if __name__ == '__main__':
    main()
