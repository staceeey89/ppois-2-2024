from Person import Person
class Speaker(Person):
    def __init__(self, name, affiliation, presentation_topic, experience_level, preferred_time):
        super().__init__(name, affiliation)
        self.__presentation_topic = presentation_topic
        self.__experience_level = experience_level
        self.__preferred_time = preferred_time
        self.__presentation_ratings = []
        self.__presentation_reviews = []

    def get_presentation_topic(self):
        return self.__presentation_topic

    def get_experience_level(self):
        return self.__experience_level

    def get_preferred_time(self):
        return self.__preferred_time

    def set_presentation_topic(self, presentation_topic):
        try:
            self.__presentation_topic = presentation_topic
        except ValueError:
            print("Тема презентации должна быть строкой.")

    def set_experience_level(self, experience_level):
        try:
            self.__experience_level = experience_level
        except ValueError:
            print("Уровень опыта должен быть 'Джуниор', 'Мидл' или 'Сеньор'.")

    def set_preferred_time(self, preferred_time):
        try:
            self.__preferred_time = preferred_time
        except ValueError:
            print("Предпочтительное время должно быть строкой.")

    def average_rating(self):
        if self.__presentation_ratings:
            return sum(self.__presentation_ratings) / len(self.__presentation_ratings)
        else:
            return None

    def display_info(self):
        print(f"Имя: {self.get_name()}")
        print(f"Членство: {self.get_affiliation()}")
        print(f"Тема презентации: {self.get_presentation_topic()}")
        print(f"Уровень опыта: {self.get_experience_level()}")
        print(f"Предпочтительное время: {self.get_preferred_time()}")
        print(f"Средняя оценка: {self.average_rating()}")
        print("Рейтинги презентаций:")
        for rating in self._Speaker__presentation_ratings:
            print(f"- {rating}")
        print("Обзоры презентаций:")
        for review in self._Speaker__presentation_reviews:
            print(f"- {review}")
