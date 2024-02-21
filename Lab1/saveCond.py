import pickle


def save_condition(camera=None, director=None, film_set=None,
                   montage=None, post_production=None, script=None, studio=None, load_number=0):
    with open('info.pickle', 'wb') as file:
        pickle.dump(camera, file)
        pickle.dump(director, file)
        pickle.dump(film_set, file)
        pickle.dump(montage, file)
        pickle.dump(post_production, file)
        pickle.dump(script, file)
        pickle.dump(studio, file)
        pickle.dump(load_number, file)
