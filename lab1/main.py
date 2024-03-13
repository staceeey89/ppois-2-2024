from irrigation_system import IrrigationSystem
from plot import Plot
from plant import Plant
from recreationArea import RecreationArea
from instrument import Instrument

instruments = []
plot = None
irrigation_system = None
recreation_area = None
a = 1

while a != 0:
    print("выберите функцию:")
    print("1. создать участок")
    print("2. посадить растение")
    print("3. ухаживать за растением")
    print("4. вывод информации о растениях на участке")
    print("5. почистить инструмент")
    print("6. приобрести инструмент")
    print("7. вывести список инструментов")
    print("8. создать систему полива")
    print("9. включить или выключить систему полива")
    print("10. полить цветы")
    print("11. заняться удобрением растений")
    print("12. создать зону отдыха")
    print("13. декорировать зону отдыха")
    print("14. все украшения зоны отдыха")
    print("15. все цветы зоны отдыха")
    print("16. заправить систему полива удобрением")
    print("0. выход")
    a = int(input())
    if a == 1:
        if plot is not None:
            print("у вас уже есть участок")
        else:
            name = input("введите тип почвы участка:")
            square = int(input("введите площадь участка:"))
            plot = Plot(name, square)
    if a == 2:
        if plot is None:
            print("вам нужно создать участок")
        else:
            name = input("какое растение вы хотите посадить:")
            plant = Plant(name)
            plot.planting_a_plant(plant, instruments)
    if a == 3:
        if plot is None:
            print("вам нужно создать участок")
        else:
            plot.print_list_of_the_plants()
            index = int(input("введите индекс растения, за которым хотите ухаживать:"))
            plot.plants[index].take_care_of()
    if a == 4:
        if plot is None:
            print("вам нужно создать участок")
        else:
            print("растения на вашем участке:")
            plot.print_list_of_the_plants()
    if a == 5:
        for index, instrument in instruments:
            print("индекс: ", index, " инструмент: ", instrument)
        name = int(input("введите индекс инструмента, который хотите почистить"))
        instruments[name].clearing()
    if a == 6:
        name = input("Какой инструмент вы хотите купить:")
        instrument = Instrument(name)
        instruments.append(instrument)
    if a == 7:
        if len(instruments) == 0:
            print("у вас нет инструментов")
        else:
            for instrument in instruments:
                print(instrument.name)
    if a == 8:
        if irrigation_system is not None:
            print("у вас уже есть система полива")
        else:
            irrigation_system = IrrigationSystem()
            print("создана система полива")
    if a == 9:
        if irrigation_system is None:
            print("у вас нет системы полива")
        else:
            print("вы хотите включить(1) или выключить(2) систему полива")
            b = int(input())
            if b == 1:
                if not irrigation_system.get_status():
                    irrigation_system.turn_on()
                else:
                    print("система уже включена")
            if b == 2:
                if irrigation_system.get_status():
                    irrigation_system.turn_off()
                else:
                    print("система уже выключена")
    if a == 10:
        if plot is None:
            print("у вас нету участка")
        if irrigation_system is None:
            print("у вас нет системы полива")
        else:
            plot.watering_my_plants(irrigation_system)
    if a == 11:
        if irrigation_system is None:
            print("у вас нет системы полива")
        elif plot is None:
            print("у вас нет участка")
        else:
            plot.fertilize_plants(irrigation_system)
    if a == 12:
        if recreation_area is not None:
            print("у вас уже есть зона отдыха")
        else:
            name = input("введите тип почвы зоны отдыха:")
            square = int(input("введите площадь зоны отдыха:"))
            recreation_area = RecreationArea(name, square)
    if a == 13:
        if recreation_area is None:
            print("у вас нет зоны отдыха")
        else:
            recreation_area.decoration(instruments)
    if a == 14:
        if recreation_area is None:
            print("у вас нет зоны отдыха")
        else:
            recreation_area.print_list_of_decorations()
    if a == 15:
        if recreation_area is None:
            print("у вас нет зоны отдыха")
        else:
            recreation_area.print_list_of_the_plants()
    if a == 16:
        if irrigation_system is None:
            print("у вас нет системы полива")
        elif irrigation_system.get_status():
            print("сначала выключите систему полива")
        elif irrigation_system.dunged:
            print("система полива уже заправлена удобрением")
        else:
            irrigation_system.start_fertilize()
    if a < 0:
        print("повторите ввод")
        a = 1
    if a > 16:
        print("повторите ввод")
        a = 1
