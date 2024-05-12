from Attraction import Attraction
from Visitor import Visitor
from SecurityRequirement import SecurityRequirement
from Queue import Queue
from AmusementPark import AmusementPark


def switch_case(argument):
    switcher = {
        1: "Add visitor",
        2: "Buy Ticket",
        3: "Choose Attraction",
        4: "View Safety Requirements",
        5: "View my tickets",
        6: "Exit"
    }
def main():

    #создаем парк и правила
    park = AmusementPark("Fun Park")
    requirement1 = SecurityRequirement("Wear seatbelt", 120, 90, 12)
    requirement2 = SecurityRequirement("Don't rock the cabin", 90, 100, 7)
    requirement3 = SecurityRequirement("Hold on to the handrails", 80, 50,5)
    requirement4 = SecurityRequirement("Hold on to the handrails", 100,60,8)

    # Создаем аттракционы
    attraction1 = Attraction("Roller Coaster", 20)
    attraction1.security_requirements.append(requirement1)
    attraction2 = Attraction("Ferris Wheel",  30)
    attraction2.security_requirements.append(requirement2)
    attraction3 = Attraction("Carousel", 15)
    attraction3.security_requirements.append(requirement3)
    attraction4 = Attraction("Flying Scooters", 10)
    attraction4.security_requirements.append(requirement4)


    park.attractions.append(attraction1)
    park.attractions.append(attraction2)
    park.attractions.append(attraction3)
    park.attractions.append(attraction4)

    visitor = Visitor()
    queue = Queue()
    while True:
        print("Menu: ")
        print("1. Add visitor's info")
        print("2. Buy Ticket")
        print("3. Choose Attraction")
        print("4. View Safety Requirements")
        print("5. View my tickets")
        print("6. Exit")

        choice = int(input("Input number: "))
        print("Your choice:", choice)
        if choice == 1:
            visitor.get_visitor_info()
        if choice == 2:
            visitor.buy_ticket(park, queue)
        elif choice == 3:
            visitor.choose_attraction(park)
        elif choice == 4:
            visitor.watch_rules(park)
        elif choice == 5:
            visitor.watch_tickets()
        elif choice == 6:
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()