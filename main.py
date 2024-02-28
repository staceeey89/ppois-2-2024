from Television import *
from Sound_system import *
from Remote_controle import *
from Technical_characteristics import *
from Screen import *
import pickle
if __name__ == "__main__":
    TV1 = Television('LG', '2500$', 'Grey')
    TV1.set_software('webOS', '3.41')
    PULT1 = Remote_control('Samsung', '250$', 'Black', TV1)
    TC = Technic_charact('17 inches', '1280x720', 'LED')

    while True:
        print("\n1. Print TV info\n2. Print Remote controle info\n3. Turn TV On\n4. Turn TV Off")
        print("5.Select Channel\n6.Adjust image(britness,contrast and saturat)\n7.Connect devices\n8.Update Software")
        print("9.Print technical info\n10.Change sound level\n11.Save data\n12.Open data\n13.Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            TV1.print_data()
        elif choice == "2":
            PULT1.print_data()
        elif choice == "3":
            PULT1.turn_tv_on()
            print("Телевизор включен?", TV1.is_on)
        elif choice == "4":
            PULT1.turn_tv_off()
            print("Телевизор включен?", TV1.is_on)
        elif choice == "5":
            PULT1.choose_new_channel('Entertainment')
        elif choice == "6":
            TV1.add_britness(80)
            TV1.add_contrast(70)
            TV1.add_saturation(100)
        elif choice == "7":
            TV1.device_connected('DVD Player', True)
        elif choice == "8":
            TV1.update_software('webOS', '3.62')
        elif choice == "9":
            TC.print_data()
        elif choice == "10":
            TV1.change_sound_level(42)
        elif choice == "11":
            with open("Television.pickle", "wb") as file:
                pickle.dump(TV1, file)
        elif choice == "12":
            with open("Television.pickle", "rb") as file:
                data = pickle.load(file)
                TV1 = data
        elif choice == "13":
            print("Exiting...")
            break
        else:
            print("Invalid choice")
