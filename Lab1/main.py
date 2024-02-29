import WorkFunctions as wf
from Montage import Montage
from Camera import Camera
from PostProduction import PostProduction
import saveCond
import loadCond
import os

montage = Montage()
camera = Camera()
post_production = PostProduction()
studio = None
film_set = None
script = None
director = None
load_number = 0

if os.path.exists("info.pickle"):
    res = loadCond.load_condition()
    camera = res[0]
    montage = res[3]
    post_production = res[4]
    load_number = res[7]
    # Загрузка состояния перед первой функцией

if load_number == 0:
    studio = wf.create_studio()
    load_number += 1
    saveCond.save_condition(camera=camera, montage=montage,
                            post_production=post_production, studio=studio, load_number=load_number)
    print("------Сохранение значений------")

if os.path.exists("info.pickle"):
    res = loadCond.load_condition()
    camera = res[0]
    montage = res[3]
    post_production = res[4]
    studio = res[6]
    load_number = res[7]
    # Загрузка состояния перед второй функцией

if load_number == 1:
    film_set = wf.create_filmset()
    load_number += 1
    saveCond.save_condition(camera=camera, montage=montage, post_production=post_production,
                            studio=studio, film_set=film_set, load_number=load_number)
    print("------Сохранение значений------")

if os.path.exists("info.pickle"):
    res = loadCond.load_condition()
    camera = res[0]
    montage = res[3]
    post_production = res[4]
    studio = res[6]
    film_set = res[2]
    load_number = res[7]
    # Загрузка состояния перед третьей функцией

if load_number == 2:
    script = wf.create_script(film_set, studio)
    load_number += 1
    saveCond.save_condition(camera=camera, montage=montage, post_production=post_production,
                            studio=studio, film_set=film_set, script=script, load_number=load_number)
    print("------Сохранение значений------")

if os.path.exists("info.pickle"):
    res = loadCond.load_condition()
    camera = res[0]
    montage = res[3]
    post_production = res[4]
    studio = res[6]
    film_set = res[2]
    script = res[5]
    load_number = res[7]
    # Загрузка состояния перед четвертой функцией

if load_number == 3:
    director = wf.create_director(script)
    load_number += 1
    saveCond.save_condition(camera=camera, montage=montage, post_production=post_production,
                            studio=studio, film_set=film_set, script=script, director=director, load_number=load_number)
    print("------Сохранение значений------")

if os.path.exists("info.pickle"):
    res = loadCond.load_condition()
    camera = res[0]
    montage = res[3]
    post_production = res[4]
    studio = res[6]
    film_set = res[2]
    script = res[5]
    load_number = res[7]
    director = res[1]
    # Загрузка состояния перед пятой функцией

if load_number == 4:
    wf.create_actors(studio)
    load_number += 1
    saveCond.save_condition(camera=camera, montage=montage, post_production=post_production,
                            studio=studio, film_set=film_set, script=script, director=director, load_number=load_number)
    print("------Сохранение значений------")

if os.path.exists("info.pickle"):
    res = loadCond.load_condition()
    camera = res[0]
    montage = res[3]
    post_production = res[4]
    studio = res[6]
    film_set = res[2]
    script = res[5]
    load_number = res[7]
    director = res[1]
    # Загрузка состояния перед шестой функцией

if load_number == 5:
    wf.create_shots(camera, montage)
    load_number += 1
    saveCond.save_condition(camera=camera, montage=montage, post_production=post_production,
                            studio=studio, film_set=film_set, script=script, director=director, load_number=load_number)
    print("------Сохранение значений------")

if os.path.exists("info.pickle"):
    res = loadCond.load_condition()
    camera = res[0]
    montage = res[3]
    post_production = res[4]
    studio = res[6]
    film_set = res[2]
    script = res[5]
    load_number = res[7]
    director = res[1]
    # Загрузка состояния перед седьмой функцией

if load_number == 6:
    wf.change_number_actors(studio, script)
    load_number += 1
    saveCond.save_condition(camera=camera, montage=montage, post_production=post_production,
                            studio=studio, film_set=film_set, script=script, director=director, load_number=load_number)
    print("------Сохранение значений------")

if os.path.exists("info.pickle"):
    res = loadCond.load_condition()
    camera = res[0]
    montage = res[3]
    post_production = res[4]
    studio = res[6]
    film_set = res[2]
    script = res[5]
    load_number = res[7]
    director = res[1]
    # Загрузка состояния перед восьмой функцией

if load_number == 7:
    wf.make_post_production(post_production, montage)
    load_number += 1
    saveCond.save_condition(camera=camera, montage=montage, post_production=post_production,
                            studio=studio, film_set=film_set, script=script, director=director, load_number=load_number)
    print("------Сохранение значений------")

if os.path.exists("info.pickle"):
    res = loadCond.load_condition()
    camera = res[0]
    montage = res[3]
    post_production = res[4]
    studio = res[6]
    film_set = res[2]
    script = res[5]
    load_number = res[7]
    director = res[1]  # Загрузка состояния перед девятой функцией

wf.make_realization(post_production, studio, script, director, montage)

saveCond.save_condition(camera=None, montage=None, post_production=None,
                        studio=None, film_set=None, script=None, director=None, load_number=0)
print("------Сохранение значений------")
