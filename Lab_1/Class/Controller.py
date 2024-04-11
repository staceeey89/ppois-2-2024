from Class.Product import *

class Controller:
    def CheckCertificate(self, product : Product):
        if product.isCertificated :
            print(f"У этого продукта есть сертификат {product.product_std.get_certificats()}")
            return True
        else:
            print("У продукта нет сертификата")
            return False

    def AddCertificate(self, product : Product, certificate_name):
        product.product_std.AddCertificate(certificate_name)
        product.isCertificated = True
        print(f"Сертификат {certificate_name} добавлен.")

    def ChangeProductInfo(self,product: Product,name,price,year):
        product.name = name
        product.price = price
        product.year = year

    def AnalysProduct(self, product : Product):
        i=0
        result = 0
        if len(product.reviews.marks) == 0:
            print("У продукта нету отзывов.")
            return -1

        while i < len(product.reviews.marks):
            result += int(product.reviews.marks[i])
            i+=1
        result = result / i
        if result < 3:
            print(f"Продукт имеет низкую оценку: {result}")
        else:
            print(f"Продукт имеет высокую оценку: {result}")
        return result

    def Recomend(self, product : Product):
        if self.AnalysProduct(product) == -1:
            print("Нельзя сделать рекомендации пока у продукта не появятся отзывы")
        else:
            review = self.AnalysProduct(product)
            print(review)

            if review < 3:
                print("Покупатели недовольны продуктом, его необходимо доработать ")
            else:
                print("Продукт хорошего качества. В доработке не нуждается")


        cert = self.CheckCertificate(product)

        if cert:
            print("В проверке не нуждается")
        else:
            print("Необходимо пройти проверку для получения сертификата")
