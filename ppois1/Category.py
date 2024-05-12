import enum


class Category(enum.StrEnum):
    food = 'food'
    clothes = 'clothes'
    medications = 'medications'
    souvenirs = 'souvenirs'
    books = 'books'
    fun = 'fun'


# print(type(Category.food.name))
# print(type(Category.food.value))

