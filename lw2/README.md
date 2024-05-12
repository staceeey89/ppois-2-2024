# Лабораторная работа №2

В рамках лабораторной работы №2 было разработано приложение, которое предназначено для управления товарами с помощью графического интерфейса, базы данных SQLite и XML файлов.

## Описание функционала

### Главное окно

На главном окне приложения представлена таблица со всеми товарами, оконное меню с возможными действиями над товарами и панель с перелистыванием страниц и выбором, сколько на странице будет товаров

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/image.png)

Сколько товаров будет на странице можно выбрать

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/amount_on_page.png)

Отображение товаров возможно в виде древовидной структуры

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/tree_view.png)

### Взаимодействие с файлами

Есть возможность создания новой базы данных или XML файла для работы

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/create_file_window.png)

Также можно открыть уже существующую базу данных или XML файл

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/open_file_window.png)

### Добавление товара

Добавить товар можно с помощью отдельного окна, после нажатия на кнопку "Добавить". Производителя можно выбрать или добавить своего

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/add_product_window.png)

При нажатии на кнопку "Добавить производителя" откроется новое окно с добавлением производителя. После этого он сразу будет выбран в качестве производителя

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/add_manufacturer_window.png)

### Поиск товара

Представлено 3 способа поиска товара: имя товара или количество на складе, имя производителя или УНП, адрес хранения

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/search_window.png)

После нажатия на кнопку "Поиск" открывается окно, в котором выводятся все товары, которые подходили под критерий

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/search_result.png)

### Удаление товара

Удаление товара возможно по тем же 3 критериям, что и поиск

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/delete_window.png)

После нажатия на кнопку удалить откроется окно с сообщением о том, сколько товаров было удалено

> ![image](https://github.com/oden73/BSUIR/blob/main/sem4/PPOIS/lw2_img/delete_message.png)
