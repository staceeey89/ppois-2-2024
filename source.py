from Menu import Menu
from Food import Food
from Order import Order
from Payment import Payment
from Feedback import Feedback
from Inventory import Inventory
from Check import Check
from Tables import Tables
from Reservation import Reservetion
from AbstractCustomer import AbstractCustomer
from Customer import Customer


def addDishToMenu(menu: Menu) -> None:
    try:
        dishName = input("Введите название блюда: ")
        dishPrice = int(input("Введите стоимость блюда: "))
        dishDescription = input("Введите описание блюда: ")
        dishIngredients = input("Введите ингридиент необходимый для приготовления блюда: ").split(", ")
        dish = Food(dishName, dishPrice, dishDescription, dishIngredients)
        menu.addItem(dish)
        print(f"Блюдо {dishName} успешно добавлено в меню")
    except ValueError:
        print("Ошибка: стоимость блюда должна быть числом.")

    
def makeOrder(order: Order, in_stock: list, menu: Menu) -> None:
    try:
        dishes = input("Что вы хотите заказать? ").split(",")
        for dish in dishes:
            dish = dish.strip()
            for item in menu.getItems():
                if item.getName() == dish:
                    order.addToOrder(item, in_stock)
                    break
            else:
                raise ValueError(f"Блюдо {dish} не найдено в меню")
    except ValueError as e:
        print(e)
            
def calculateTheOrder(order: Order) -> None:
    try:
        listOrder = order.getTheOrder()
        if not listOrder:
            raise ValueError
        for position in listOrder:
            print(f"Название блюда: {position.getName()}")
            print(f"К оплате: {position.getPrice()}руб")
    except ValueError:
        print("The order is empty")    
        
def payTheBill(order: Order, money: Payment, customer: Customer) -> None:
    if not order.getTheOrder():
        raise ValueError("Заказ пустой.")
    order_succeed = money.pay(order, customer)
    if order_succeed:
        choice = input("Оплата прошла, печатать чек? ")
        if choice == "yes":
            check = Check(order, order_succeed)
            check.generate_check()
        else:
            print("Приятного аппетита")
        order._list_order = []
    else:
        print("Недостаточно средств")
        
def chooseTheTable(tables: Tables, customer: AbstractCustomer) -> None:
    try:
        if customer.didTookTable():
            raise ValueError("Вы уже заняли столик")
    except ValueError as e:
        print(e)
        return
    try:
        tables.getInfo()
        while True:
            tableNumber = int(input("Введите номер столика: "))
            tableChosen = tables.takeTable("Number " + str(tableNumber), customer)
            if tableChosen:
                break
    except ValueError:
        print("Ошибка: номер столика должен быть числом")
    
def reserveTheTable(reservetion: Reservetion, tables: Tables, customer: AbstractCustomer) -> None:
    try:
        if customer.didTookTable():
            raise ValueError("Вы уже заняли столик")
    except ValueError as e:
        print(e)
        return
    reservetion.getInfo()
    while True:
        tableNumber = input("Введите номер столика: ")
        tableChosen = reservetion.takeTable("Number " + tableNumber, tables, customer)
        if tableChosen:
            break
    
def leaveFeedback(customer: Customer, feedback: Feedback) -> None:
    if customer.Ordered():
        review = input("Напишите отзыв: ")
        feedback.addFeedback(review)
    else:
        print("Firstly you need to order smth")
        
def checkFeedbacks(feedback: Feedback) -> None:
    print("Отзывы: ")
    feedbacks = feedback.getFeedbacks()
    for comment in feedbacks:
        print(comment)


def main():
    menu = Menu()
    money = Payment(150)
    ingr_in_stock = Inventory()
    order = Order()
    in_stock = ["Мука", "Сахар", "Яйца", "Овощи", "Фрукты", "Тесто", "Мясо", "Специи", "Масло", "Соус"]
    tables_info = {
        "Number 1": "Free",
        "Number 2": "Reserved",
        "Number 3": "Occupied",
        "Number 4": "Free"
    }
    tables = Tables(tables_info)
    reservetion = Reservetion(tables_info)
    customer = Customer()
    feedbacks = Feedback()


    while True:
        print("\nМеню:")
        print("1. Добавить блюдо в меню")
        print("2. Сделать заказ")
        print("3. Обработать заказ")
        print("4. Оплатить счет")
        print("5. Выбрать столик")
        print("6. Забронировать столик")
        print("7. Просмотреть отзывы")
        print("8. Оставить отзыв")
        print("9. Выход")
            
        choice = input("Выберите действие: ")
        
        if choice == "1":
            addDishToMenu(menu)
            
        elif choice == "2":
            makeOrder(order, in_stock, menu)
            
        elif choice == "3":
            calculateTheOrder(order)
            
        elif choice == "4":
            try:
                payTheBill(order, money, customer)
            except ValueError as e:
                print(e)
            
        elif choice == "5":
            chooseTheTable(tables, customer)
            
        elif choice == "6":
            reserveTheTable(reservetion, tables, customer)
            
        elif choice == "7":
            checkFeedbacks(feedbacks)
            
        elif choice == "8":
            leaveFeedback(customer, feedbacks)
        
        elif choice == "9":
            break
        
if __name__ == "__main__":
    main()