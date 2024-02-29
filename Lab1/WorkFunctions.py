from Director import Director
from Studio import Studio
from FilmSet import FilmSet
from Script import Script
from Actor import Actor


def create_studio():
    # Создаем студию
    studio_name = str(input("Введите название студии: "))
    while True:
        try:
            studio_number = int(input("Введите кол-во актеров: "))

            while studio_number <= 0:
                studio_number = int(input("Измените кол-во актеров! "))
            break

        except ValueError:
            print("Введите целое число число. ")

    while True:
        try:
            old_number = int(input("Введите кол-во старых актеров: "))
            young_number = int(input("Введите кол-во молодых актеров: "))

            while old_number + young_number != studio_number:
                print("Кол-во актеров не совпадает. ")
                old_number = int(input("Кол-во старых актеров: "))
                young_number = int(input("Кол-во молодых актеров: "))
            break

        except ValueError:
            print("Введите целое число число. ")

    studio = Studio(studio_name, studio_number)
    studio.set_young_old_numbers(young_number, old_number)
    print("Студия найдена.")
    print("---------------")
    return studio


def create_filmset():
    # Создаем площадку для студии
    filmset_type = str(input("Введите тип площадки под фильм: "))
    film_set = FilmSet(filmset_type)
    print("Площадка найдена. ")
    print("---------------")
    return film_set


def create_script(film_set, studio):
    # Создадим сценарий для фильма
    script_name = str(input("Введите название  в сценарии: "))
    script_type = str(input("Введите тип сценария (должен совпадать с типо площадки): "))

    while script_type != film_set.get_film_set_type():
        script_type = str(input("Этот тип не подходит. Введите другой: "))
    while True:
        try:
            script_person_number = int(input("Введите кол-во актеров: "))
            while (script_person_number <= 0) or (script_person_number != studio.get_person_number()):
                script_person_number = int(input("Введите корректное кол-во актеров: "))
            break

        except ValueError:
            print("Введите целое число. ")

    while True:
        try:
            script_experience = int(input("0 - начальный, 1 - средний, 2 - профессиональный директор: "))

            while (script_experience < 0) or (script_experience > 2):
                script_experience = int(input("Введите корректный опыт режиссера: "))
            break
        except ValueError:
            print("Введите целое число. ")

    script_plot = str(input("Введите описание фильма: "))

    script = Script(script_name, script_type, script_person_number, script_plot, script_experience)
    print("Сценарий создан.")
    print("---------------")
    return script


def create_director(script):
    # Создадим режиссера для фильма
    director_name = str(input("Введите название режиссера: "))
    director = Director(director_name)
    director_exp = 0
    while (director.get_experience() < script.get_experience_director()) or ((director_exp < 0) or (director_exp > 2)):
        print("Опыт режиссера мал или некорректен. Обучите его.")
        while True:
            try:
                director_exp = int(input("0 - начальный, 1 - средний, 2 - профессиональный "))
                break
            except ValueError:
                print("Введите целое число. ")
        director.change_experience(director_exp, script)
    print("Режиссер найден.")
    print("---------------")
    return director


def create_actors(studio):
    # Создадим актеров
    while studio.compare_numbers_people():
        actor_name = str(input("Введите имя актера: "))
        print("Выбирайте актеров: до 40 молодой, после 40 - взрослый ")
        while True:
            try:
                actor_age = int(input())
                break
            except ValueError:
                print("Введите целое число. ")
        actor = Actor(actor_name, actor_age)
        if len(studio.get_list_old_persons()) + len(studio.get_list_young_persons()) < studio.get_person_number():
            studio.add_person(actor)
        else:
            print("Актеров слишком много.")
    return True

def create_shots(camera, montage):
    print("Снимаем кадры фильма")
    camera_pos = None
    while camera_pos != "e":
        print("r - повернуть вправо, l - повернуть влево, u - повернуть вверх, d - повернуть вниз, e - выход ")
        camera_pos = str(input())

        if camera_pos == "r":
            camera.turn_right(montage)
        elif camera_pos == "l":
            camera.turn_left(montage)
        elif camera_pos == "u":
            camera.turn_up(montage)
        elif camera_pos == "d":
            camera.turn_down(montage)
        elif camera_pos == "e":
            break
        else:
            print("Некорректное значение.")
    return True


def make_post_production(post_production, montage):
    # Делаем постпродакшн
    p_p_change = None

    print("Постпродакшен фильма")
    while p_p_change != "e":
        print("del - удалить слайд, ch - изменить расположение слайда, e - выход: ")
        p_p_change = input()

        if p_p_change == "del":
            while True:
                try:
                    del_pos = int(input("Позиция, которую надо удалить: "))
                    break
                except ValueError:
                    print("Введите целое число.")
            post_production.del_shot(del_pos, montage)
        elif p_p_change == "ch":
            while True:
                try:
                    old_pos = int(input("Укажите позицию кадра: "))
                    new_pos = int(input("Укажите новую позицию: "))
                    break
                except ValueError:
                    print("Введите целое число")
            post_production.change_shot_place(new_pos, old_pos, montage)
        elif p_p_change == "e":
            break
        else:
            print("Некорректные данные.")
    return True


def make_realization(post_production, studio, script, director, montage):
    print("Реализация:")
    post_production.make_realization(studio, script, director, montage)
    return True


def change_number_actors(studio, script):
    while True:
        change = str(input("ch - изменить кол-во актеров, e - выход "))
        if change == "ch":
            while True:
                try:
                    number = int(input("Введите новое кол-во актеров: "))
                    break
                except ValueError:
                    print("Введите целое число.")
            studio.set_number_people(number, script)
        elif change == "e":
            break
        else:
            print("Некорректное значение.")
    return True
