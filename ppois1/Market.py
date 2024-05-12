
from Customer import Customer
from Merchant import Merchant
from Category import Category
from Product import Product
from Tradestand import TradeStand
from Place import Place


class Market:
    def __init__(self, merchants: list[Merchant], customer: Customer):
        self.__merchants = merchants
        self.__customer = customer

    def ads(self):
        return """Did you know about this new medieval market in town?
                     Well...
                     Now you do! You are all welcome to walk, eat, drink, 
                     get excited and just have fun with your family!"""

    def trade(self):
        bought = False
        found, merchant = self.find_need_match()
        if not found:
            print("We're sorry, but it seems there's no merchant or place that could fulfill your need")
            return
        else:
            if self.__customer.get_need() == 'fun':
                print("Welcome to our amusement park! ")
                print("Choose a ticket to an attraction you'd like to buy:")
            else:
                print("Choose a product you'd like to buy:")
                for i in range(len(merchant.get_place().get_stands())):
                    print(f"{i + 1} - {merchant.get_place().get_stands()[i].get_product().get_name()}: "
                          f"{merchant.get_place().get_stands()[i].get_product().get_price()} solids")
                product = input("")
                try:
                    product_num = int(product)
                    selected_product = merchant.get_place().get_stands()[product_num - 1].get_product()
                    bought = self.__specific_trade(selected_product, merchant)
                except ValueError:
                    print("It appears, you entered an incorrect parameter")
                return bought

    def find_need_match(self):
        found = False
        right_merchant = 0
        for merchant in self.__merchants:
            c_need = self.__customer.get_need()
            m_need = merchant.get_place().get_need()
            if c_need == m_need:
                found = True
                right_merchant = merchant
                break
        return found, right_merchant

    def info(self):
        print("Our market members and their products:")
        for merchant in self.__merchants:
            print(f"{merchant.get_name()}")
            merchant.get_place().print_stands()

    def get_customer(self) -> Customer:
        return self.__customer

    def get_merchants(self) -> list[Merchant]:
        return self.__merchants

    def __specific_trade(self, product: Product, merchant: Merchant = None) -> bool:
        if merchant is None:
            found, merchant = self.find_need_match()
        if self.__customer.get_cunning():
            print("You: How much you say??? I will tell the hole town about your nonsense!")
            new_product = merchant.make_discount(product)
        else:
            new_product = product
        bought = self.__customer.buy(new_product)
        if bought:
            merchant.sell(new_product)
            if self.__customer.get_need() == 'fun':
                print("Yuppieee! That was so fun, wasn't it?")
        else:
            print("Oops! It appears you dont have enough money:(")
        return bought




