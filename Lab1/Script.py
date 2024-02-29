class Script:
    def __init__(self, name="", film_type="", actors_number=0, plot="", experience_director=0):
        self._name = str(name)
        self._film_type = str(film_type)
        self._actors_number = int(actors_number)
        self._plot = str(plot)
        self._experience_director = int(experience_director)

    def get_name(self):
        return self._name

    def set_actors_number(self, num):
        self._actors_number = num

    def get_film_type(self):
        return self._film_type

    def get_actors_number(self):
        return self._actors_number

    def get_plot(self):
        return self._plot

    def get_experience_director(self):
        return self._experience_director
