from colorama import Fore

class CLI():
        
    def print_menu() -> None:

        print(Fore.CYAN + "0) Exit")
        print("1) Add standart driver")
        print("2) Create driver and add it")
        print("3) Change curr. driver")
        print("4) Add standart car-kit to curr. driver")
        print("5) Create car and add it to curr. driver")
        print("6) Change curr. car")
        print("7) Remove car from car-list in curr. driver")
        print("8) Drive curr. car")
        print("9) Curr. car service")
        print("10) Info about current driver")
        print("11) Drivers list")
        print("12) Help\n")

    def print_drive_menu() -> None: 

        print(Fore.CYAN +"0) Stop driving and engine")
        print("1) Start engine")
        print("2) Change gear")
        print("3) Drive forward")
        print("4) Drive back")
        print("5) Drive right")
        print("6) Drive left")
        print("7) Car state\n")

    def print_gears() -> None:

        print(Fore.CYAN +"0) N: Neutral")
        print("1) R: Reverse")
        print("2) G1: First gear")
        print("3) G2: Second gear")
        print("4) G3: Third gear")
        print("5) G4: Fourth gear\n")

    def print_service_menu() -> None:

        print(Fore.CYAN + "0) Exit from service")
        print("1) Add car to gasstation-queue")
        print("2) Remove car from gasstation-queue")
        print("3) Add all vehicle fleet to gasstation-queue")
        print("4) Refueling all cars in gasstation-queue")
        print("5) Repair curr. car")
        print("6) Change oil in curr. car")
        print("7) Car state\n")

    def exit_from_service() -> None: print("Have been returned to main menu\n")