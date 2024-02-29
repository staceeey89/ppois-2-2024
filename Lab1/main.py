from barbershop import Barbershop
import pickle


def main_menu():
    print("\n1. Добавить запись ")
    print("2. Просмотр записей ")
    print("3. Выполнить все записанные услуги ")
    print("4. Закупка оборудования и найм работников ")
    print("5. Посмотреть текущий бюджет ")
    print("0. Сохранить состояние и выйти")


def registration_menu():
    name = input("Введите имя клиента: ")
    time = input("Введите время записи в виде числа от 8 до 19: ")
    day = input('Введите день записи в виде числа от 1 до 7: ')
    service_type = input("Выберите тип услуги\n 1. Стрижка \n 2. Укладка \n 3. Консультация по уходу за волосами: ")
    hair_length = input("Введите длину волос в сантиметрах ")
    hair_type = input("Укажите тип волос: 1: тонкие 2: жесткие ")
    try:
        response = best_barber.add_registration(name, day, time, service_type, hair_length, hair_type)
        print(response)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    file_name = "barbershop_state.pkl"
    try:
        best_barber = Barbershop(0)
        best_barber.load_state(file_name)
        print("Состояние успешно загружено.")
    except FileNotFoundError:
        budget = input("Введите начальный бюджет парикмахерской:")
        best_barber = Barbershop(budget)
    while True:
        main_menu()
        choice = input("Введите номер действия: ")
        if choice == "1":
            if best_barber.barbers_not_empty():
                registration_menu()
            else:
                print("Добавьте работников для возможности записывать клиентов ")
        elif choice == "2":
            print(best_barber.print_all_registrations())
            choice = input("Введите номер записи для её удаления \n Введите 0 чтоб перейти в главное меню  ")
            best_barber.delete_registration(choice)
        elif choice == "3":
            print(best_barber.perform_all_registered_services())
        elif choice == "4":
            print(best_barber.purchase())
        elif choice == "5":
            print(f"Бюджет: {best_barber.budget} ")
        elif choice == "0":
            best_barber.save_state(file_name)
            break
        else:
            print("Выберите существующий пункт меню.")
