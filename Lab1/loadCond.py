import pickle


def load_condition():
    with open('info.pickle', 'rb') as file:
        camera = pickle.load(file)
        director = pickle.load(file)
        film_set = pickle.load(file)
        montage = pickle.load(file)
        post_production = pickle.load(file)
        script = pickle.load(file)
        studio = pickle.load(file)
        load_number = pickle.load(file)

    return camera, director, film_set, montage, post_production, script, studio, load_number
