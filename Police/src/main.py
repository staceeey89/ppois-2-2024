import datetime
import pickle
from police import Police
from config.constants import OFFICERS_PATH, POLICE_SAVE, OFFICERS_SAVE
from utils.utils import Loader

if __name__ == '__main__':
    try:
        with open(OFFICERS_SAVE, 'rb') as f:
            officer_list: list = pickle.load(f)
    except FileNotFoundError:
        officer_list: list = Loader.load_officers(OFFICERS_PATH)

    try:
        with open(POLICE_SAVE, 'rb') as f:
            police: Police = pickle.load(f)
    except FileNotFoundError:
        print("Добрый день. Добро пожаловать в ""Модель полиции"".")

        location = input("Для того, чтобы продолжить введите город, где находится ваш полицейский участок: ")
        print(f"У вас в участке работает {len(officer_list)} полицейских.")
        name = input("Введите ваше имя, чтобы знать как к вам обращаться: ")
        print(f"Отлично, {name}")
        police = Police(location, name, officer_list)
        with open(POLICE_SAVE, 'wb') as f:
            pickle.dump(police, f)
        print("Теперь можно приступать к вашей первой смене в новой должности!")

    user_choice = input("Нажмите Y - чтобы начать смену, любую другую кнопку - чтобы выйти: ")
    if user_choice.upper() == "Y":
        start_time = datetime.datetime(2024, 2, 21, 8)
        while True:
            police.prepare_duty(start_time)
            police.on_duty()
            police.off_duty()

            user_choice = input("Нажмите любую кнопку - чтобы продолжить, N - чтобы выйти: ")
            if user_choice.upper() == "N":
                break
            start_time += datetime.timedelta(days=1)
    print("Вы вышли.")

    with open(POLICE_SAVE, 'wb') as f:
        pickle.dump(police, f)

    with open(OFFICERS_SAVE, 'wb') as f:
        pickle.dump(officer_list, f)
