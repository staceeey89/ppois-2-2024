from Class.Review import *
from Class.Standard import *


class Product:
    reviews = Review()

    isCertificated = False

    def __init__(self, name, price, year):
        self.name = name
        self.price = price
        self.year = year
        self.product_std = Standard("Нету стандарта")
        print(f"Продукт {name} был добавлен")

    def AddReview(self, review, mark): #Добавление отзыва
        self.reviews.AddComm(review,mark)
        return "Отзыв добавлен"

    def AddStandart(self, std_name):
        self.product_std.set_standart(std_name)
        return std_name

    def PrintReview(self):
        self.reviews.PrintComms()
        return True

    def PrintInfo(self):
        print(f"Название продукта: {self.name}")
        print(f"Цена продукта: {self.price}")
        print(f"Год выпуска продукта: {self.year}")
        print()
        print("Отзывы о продукте: ")
        print()
        print(f'Стандарт продукта: {self.product_std.get_standart()}')
        self.PrintReview()