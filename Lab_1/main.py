from Class.Controller import *
from Class.Product import *

# Создание объекта контроллера
control = Controller()

def print_menu():
    print("Меню:")
    print("1. Добавить продукты")
    print("2. Добавить Отзыв продукту")
    print("3. Показать отзывы о продукте")
    print("4. Проверить наличие сертификата")
    print("5. Добавить сертификат")
    print("6. Анализ продукта")
    print("7. Рекомендации для продукта")
    print("8. Добавить номер Стандарта продукта")
    print("9. Информация о продукте")
    print("10. Выход")

def product_choice(products):
    print("Список всех продуктов:")
    num = 1
    for product in products:
        print(f"{num}. {product.name}")
        num += 1
    try:
        choice = int(input("Выберите номер продукта: "))
    except:
        print("Ошибка ввода :( ")
        product_choice(products)
    return choice-1


# Главный цикл программы
while True:
    print("----"*8)
    print_menu()
    try:
        choice = input("Выберите опцию (1-10): ")
    except:
        print("Ошибка ввода :( ")
        break

    if choice == "1":
        try:
            num_products = int(input("Введите количество продуктов: "))
        except:
            print("Вы ввели не число")
            continue
        # Создание списка для хранения
        products = []

        # Цикл для создания объектов
        for i in range(num_products):
            print(f"\nПродукт {i + 1}")
            try:
                name = str(input("Введите название продукта: "))
                price = int(input("Введите цену продукта: "))
                year = int(input("Введите год выпуска продукта: "))
            except:
                print("Ошибка ввода информации о продукте")
                continue

            product = Product(name, price, year)
            products.append(product)

    elif choice == "2":
        choice = product_choice(products)
        review = input("Введите отзыв: ")
        mark = input("Введите оценку: ")
        products[choice-1].AddReview(review,mark)

    elif choice == "3":
        choice = product_choice(products)
        products[choice-1].PrintReview()

    elif choice == "4":
        choice = product_choice(products)
        control.CheckCertificate(products[choice])

    elif choice == "5":
        choice = product_choice(products)
        certificate = input("Введите номер сертификата: ")
        control.AddCertificate(products[choice], certificate)

    elif choice == "6":
        choice = product_choice(products)
        control.AnalysProduct(products[choice])

    elif choice == "7":
        choice = product_choice(products)
        control.Recomend(products[choice])

    elif choice == "8":
        choice = product_choice(products)
        stand = input("Введите название стандарта: ")
        products[choice].AddStandart(stand)

    elif choice == "9":
        choice = product_choice(products)
        products[choice].PrintInfo()

    elif choice == "10":
        print("Программа завершена.")
        break

    else:
        print("Некорректный выбор. Попробуйте еще раз.")

