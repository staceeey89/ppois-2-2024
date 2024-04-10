import unittest

from Class.Controller import *

prod = Product("Ноутбук", 3000, 2019)
prod2 = Product("Монитор", 2000, 2015)
prod3 = Product("Клавиатура", 500, 2020)
control = Controller()
print('****'*8)

class MyTestCase(unittest.TestCase):

    def test_controller_review(self):
        self.assertEqual(control.AnalysProduct(prod3),5)

    def test_product_review(self):
        self.assertEqual(prod.AddReview("Хороший ноутбук", 5), "Отзыв добавлен")

    def test_analys(self):
        prod2.AddReview("Хороший монитор", 5)
        self.assertEqual(control.AnalysProduct(prod2), 5)

    def test_product_standart(self):
        self.assertEqual(prod.AddStandart("010101"), "010101")

    def test_controller_cert_1(self):
        self.assertEqual(control.CheckCertificate(prod), False)

    def test_controller_cert_2(self):
        control.AddCertificate(prod, "Сертификат Качества")
        self.assertEqual(control.CheckCertificate(prod), True)

    def test_product_print_review(self):
        self.assertEqual(prod2.PrintReview(),True)

    def test_standart1(self):
        self.assertEqual(prod2.product_std.get_standart(), "Нету стандарта")

    def test_standart2(self):
        self.assertEqual(prod.product_std.get_standart(), "010101")

    def test_standart3(self):
        prod3.product_std.set_standart("2057794")
        self.assertEqual(prod3.product_std.get_standart(), "2057794")



if __name__ == '__main__':
    unittest.main()
