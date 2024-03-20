import pickle
import os
import exception
from room import Room
from vacuum_cleaner import VacuumCleaner

if __name__ == '__main__':
    if not os.path.isfile("resources/data.pickle") or os.path.getsize("resources/data.pickle") == 0:
        print("У вас отсутствует пылесос. Следует создать его.")
        choose_color = input("Введите цвет пылесоса: ")
        choose_firm = input("Введите фирму пылесоса: ")
        new_vacuum_cleaner = VacuumCleaner(choose_color, choose_firm)
        choose_min_power = int(input("Введите минимальную мощность(Вт): "))
        choose_max_power = int(input("Введите максимальную мощность(Вт): "))
        new_vacuum_cleaner.engine.set_power(choose_min_power, choose_max_power)
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(new_vacuum_cleaner, file)
    else:
        with open("resources/data.pickle", "rb") as file:
            new_vacuum_cleaner = pickle.load(file)
            print(f"Используемый пылесос: \n\tФирма: {new_vacuum_cleaner.firm}\n\tЦвет: {new_vacuum_cleaner.color}")

while True:
    choose_action = input("\n🕹Управление пылесосом:\n\t1.Запустить пылесос\n\t2.Выбрать насадку"
                          "\n\t3.Посмотреть засоренность фильтра"
                          "\n\t4.Посмотреть засорен ли контейнер для пыли\n\t5.Посмотреть какая насадка надета"
                          "\n\t6.Изменить текущую мощность\n\t7.Посмотреть установленную мощность\n\n🧹Уборка:"
                          "\n\t8.Выполнить уборку помещения\n\n⚙️Обслуживание пылесоса:\n\t9.Заменить фильтр"
                          "\n\t10.Очистить контейнер для пыли\n\t11.Заменить насадку"
                          "\n\t12.Выполнить техническое обслуживание\n\n❌ 13.Выход\n\nВаш выбор: ")
    if choose_action == "1":
        with open("resources/data.pickle", "rb") as file:
            new_vacuum_cleaner = pickle.load(file)
        if new_vacuum_cleaner.control_buttons.start_b:
            print("Пылесос уже запущен.")
            continue
        set_power = int(input("Введите текущую мощность(Вт): "))
        if set_power < new_vacuum_cleaner.engine.min_power or set_power > new_vacuum_cleaner.engine.max_power:
            raise exception.InvalidPowerValue("‼️ Введены неверные значения")
        new_vacuum_cleaner.start_vacuum(set_power)
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(new_vacuum_cleaner, file)
    elif choose_action == "2":
        with open("resources/data.pickle", "rb") as file:
            new_vacuum_cleaner = pickle.load(file)
        choose_nozzle = input("Выберите насадку(Turbo Brush, Slot Nozzle, Round Nozzle, Laminate Nozzle, "
                              "Corner Nozzle).\nВведите аналогично предложенным: ")
        new_vacuum_cleaner.put_on_nozzle(choose_nozzle)
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(new_vacuum_cleaner, file)
    elif choose_action == "3":
        new_vacuum_cleaner.check_filter_health()
    elif choose_action == "4":
        new_vacuum_cleaner.check_dust_container()
    elif choose_action == "5":
        new_vacuum_cleaner.show_nozzle()
    elif choose_action == "6":
        with open("resources/data.pickle", "rb") as file:
            new_vacuum_cleaner = pickle.load(file)
        wishful_power = int(input("Введите мощность, которую хотите установить: "))
        if wishful_power < new_vacuum_cleaner.engine.min_power or wishful_power > new_vacuum_cleaner.engine.max_power:
            raise exception.InvalidPowerValue("‼️ Введены неверные значения")
        new_vacuum_cleaner.control_buttons.change_power(wishful_power)
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(new_vacuum_cleaner, file)
    elif choose_action == "7":
        new_vacuum_cleaner.show_power()
    elif choose_action == "8":
        with open("resources/data.pickle", "rb") as file:
            new_vacuum_cleaner = pickle.load(file)
        choose_length = int(input("Введите размеры комнаты, которую хотите убрать\nДлина: "))
        choose_width = int(input("Ширина: "))
        if not new_vacuum_cleaner.control_buttons.start_b:
            raise exception.InvalidButtonException("‼️Пылесос не запущен. Запустите его")
        elif new_vacuum_cleaner.dust_container.isFilled:
            raise exception.InvalidButtonException("‼️ Контейнер для пыли заполнен. Очистите его")
        elif new_vacuum_cleaner.filter.health <= 0:
            raise exception.InvalidFilterHealthValue("‼️ Фильтр засорен. Сначала очистите его.")
        elif not (new_vacuum_cleaner.nozzle.slot_nozzle or new_vacuum_cleaner.nozzle.turbo_brush or
                  new_vacuum_cleaner.nozzle.round_nozzle or new_vacuum_cleaner.nozzle.corner_nozzle or
                  new_vacuum_cleaner.nozzle.laminate_nozzle):
            raise exception.InvalidNozzleValue("‼️ У вас отсутствует насадка. Сначала наденьте её.")
        else:
            dust_room = Room(choose_length, choose_width)
            new_vacuum_cleaner.clean_room(dust_room)
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(new_vacuum_cleaner, file)
    elif choose_action == "9":
        with open("resources/data.pickle", "rb") as file:
            new_vacuum_cleaner = pickle.load(file)
        new_vacuum_cleaner.change_filter()
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(new_vacuum_cleaner, file)
    elif choose_action == "10":
        with open("resources/data.pickle", "rb") as file:
            new_vacuum_cleaner = pickle.load(file)
        new_vacuum_cleaner.clean_dust_container()
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(new_vacuum_cleaner, file)
    elif choose_action == "11":
        with open("resources/data.pickle", "rb") as file:
            new_vacuum_cleaner = pickle.load(file)
        choose_nozzle = input("Выберите насадку(Turbo Brush, Slot Nozzle, Round Nozzle, Laminate Nozzle, "
                              "Corner Nozzle).\nВведите аналогично предложенным: ")
        new_vacuum_cleaner.change_nozzle(choose_nozzle)
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(new_vacuum_cleaner, file)
    elif choose_action == "12":
        with open("resources/data.pickle", "rb") as file:
            new_vacuum_cleaner = pickle.load(file)
        new_vacuum_cleaner.technical_work()
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(new_vacuum_cleaner, file)
    elif choose_action == "13":
        break
    else:
        print("‼️ Неверный ввод ‼️")
