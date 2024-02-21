class FilmSet:
    def __init__(self, film_set_type=""):
        self._film_set_type = str(film_set_type)

    def get_film_set_type(self):
        return self._film_set_type

