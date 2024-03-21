from Customer import Customer
from Merchant import Merchant
from Product import Product
from Tradestand import TradeStand
from Place import Place
from Market import Market
import sys


def create(customer: Customer = 0) -> Market:
    product1 = Product("carrot", 3)
    product2 = Product("tomato", 4)
    product3 = Product("beef", 10)
    trade_stand1 = TradeStand(product1, 7)
    trade_stand2 = TradeStand(product2, 6)
    trade_stand3 = TradeStand(product3, 9)
    place1 = Place([trade_stand1, trade_stand2, trade_stand3], 'food')
    merchant1 = Merchant("Franko", 56, place1)
    product4 = Product("hat", 12)
    product5 = Product("socks", 5)
    trade_stand4 = TradeStand(product4, 5)
    trade_stand5 = TradeStand(product5, 20)
    place2 = Place([trade_stand4, trade_stand5], 'clothes')
    merchant2 = Merchant("Antonio", 45, place2)
    product6 = Product("sage", 5)
    product7 = Product("eucalyptus", 7)
    product8 = Product("camomile", 3)
    trade_stand6 = TradeStand(product6, 15)
    trade_stand7 = TradeStand(product7, 20)
    trade_stand8 = TradeStand(product8, 20)
    place3 = Place([trade_stand6, trade_stand7, trade_stand8], 'medications')
    merchant3 = Merchant("Roberto", 38, place3)
    product9 = Product("magnet", 1)
    product10 = Product("pen", 2)
    trade_stand9 = TradeStand(product9, 30)
    trade_stand10 = TradeStand(product10, 25)
    place4 = Place([trade_stand9, trade_stand10], 'souvenirs')
    merchant4 = Merchant("David", 28, place4)
    product11 = Product("Master and Margarita", 30)
    product12 = Product("Idiot", 35)
    trade_stand11 = TradeStand(product11, 3)
    trade_stand12 = TradeStand(product12, 2)
    place5 = Place([trade_stand11, trade_stand12], 'books')
    merchant5 = Merchant("Sebastian", 60, place5)
    attraction1 = Product("carousel", 10)
    attraction2 = Product("bench", 7)
    attraction3 = Product("knight play", 15)
    trade_stand13 = TradeStand(attraction1, 15)
    trade_stand14 = TradeStand(attraction2, 15)
    trade_stand15 = TradeStand(attraction3, 7)
    place6 = Place([trade_stand13, trade_stand14, trade_stand15], 'fun')
    merchant6 = Merchant("Federico", 33, place6)
    if customer:
        my_customer = customer
    else:
        c_name = input("How would you like to name a customer you want to play as: ")
        c_pre_age = input("Please enter their age: ")
        try:
            c_age = int(c_pre_age)
        except ValueError:
            print("It appears, you entered an incorrect parameter")
        c_str_cunning = input("Would you like for them to be cunning;)(True -'T' aor False - 'F') : ")
        if c_str_cunning == "T":
            c_cunning = True
        elif c_str_cunning == "F":
            c_cunning = False
        else:
            print("It appears, you entered an incorrect parameter")
            c_cunning = False
        c_pre_budget = input("Please enter their budget: ")
        try:
            c_budget = int(c_pre_budget)
        except ValueError:
            print("It appears, you entered an incorrect parameter")
            sys.exit(0)

        print(""" Now for needs: 
        1 - food
        2 - clothes
        3 - medications
        4 - souvenirs
        5 - books
        6 - just have fun at an amusement park""")
        try:
            c_num_need = int(input(""))
            if c_num_need == 1:
                c_need = 'food'
            if c_num_need == 2:
                c_need = 'clothes'
            if c_num_need == 3:
                c_need = 'medications'
            if c_num_need == 4:
                c_need = 'souvenirs'
            if c_num_need == 5:
                c_need = 'books'
            if c_num_need == 6:
                c_need = 'fun'
            if c_num_need > 6:
                print("It appears, you entered an incorrect parameter")
                c_need = ''
        except ValueError:
            print("It appears, you entered an incorrect parameter")
            sys.exit(0)
        my_customer = Customer(c_name, c_age, c_cunning, c_budget, c_need)
    my_market = Market([merchant1, merchant2, merchant3, merchant4, merchant5, merchant6], my_customer)
    return my_market


def main():
    my_market = create()
    while True:
        print("Welcome to Medieval Market!"
              "All our activities are listed down below. "
              "Please select one of them:")
        print("""
                 1 - see ads
                 2 - see our merchants and their products
                 3 - trade 
                 4 - visit the tavern(18+)
                 5 - leave""")
        try:
            i = int(input(''))
            match i:
                case 1:
                    my_market.ads()
                case 2:
                    my_market.info()
                case 3:
                    my_market.trade()
                case 4:
                    my_market.get_customer().visit_tavern()
                case 5:
                    return "We will miss you! Dont forget to tell your friends about us!"
        except ValueError:
            print("It appears, you entered an incorrect parameter")


if __name__ == "__main__":
    main()
