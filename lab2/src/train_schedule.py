import sqlite3
import random

connect = sqlite3.connect("../database/train.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS information_board (
                train_number INTEGER NOT NULL,
                departure_station TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_station TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                travel_time TEXT NOT NULL)""")

# cities = ["Минск", "Гомель", "Могилев", "Витебск", "Гродно", "Брест", "Бобруйск", "Барановичи", "Борисов", "Пинск",
#           "Орша", "Мозырь", "Солигорск", "Новополоцк", "Лида", "Молодечно", "Светлогорск", "Жлобин", "Слуцк", "Речица"]
cities = ["Москва", "СанктПетербург", "Новосибирск", "Екатеринбург", "НижнийНовгород", "Казань", "Челябинск",
          "Омск", "Самара", "РостовнаДону", "Уфа", "Красноярск", "Пермь", "Воронеж", "Волгоград", "Краснодар",
          "Саратов", "Тюмень", "Тольятти", "Ижевск"]

# Вставка 50 строк в таблицу
for _ in range(20):
    train_number = random.randint(100, 999)
    departure_station = random.choice(cities)
    arrival_station = random.choice(cities)
    departure_time = f"2023-05-{random.randint(1, 31):02d} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
    arrival_time = f"2023-05-{random.randint(1, 31):02d} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
    travel_time = f"{random.randint(0, 5)} days, {random.randint(0, 23)} hours, {random.randint(0, 59)} minutes"

    cursor.execute("INSERT INTO information_board VALUES (?, ?, ?, ?, ?, ?)",
                   (train_number, departure_station, departure_time, arrival_station, arrival_time, travel_time))

connect.commit()

connect.close()