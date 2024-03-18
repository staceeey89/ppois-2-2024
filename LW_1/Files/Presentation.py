from Speaker import Speaker
class Presentation:
    def __init__(self, title, speaker: Speaker, topic):
        try:
            self.__title = title
            self.__speaker = speaker
            self.__topic = topic
            self.__slides = []
        except TypeError:
            raise TypeError("Аргумент speaker должен быть экземпляром класса Speaker.")

    def get_title(self):
        return self.__title

    def get_speaker(self):
        return self.__speaker

    def get_topic(self):
        return self.__topic

    def set_title(self, title):
        try:
            self.__title = title
        except ValueError:
            print("Заголовок должен быть строкой.")

    def set_speaker(self, speaker):
        try:
            self.__speaker = speaker
        except TypeError:
            print("Аргумент speaker должен быть экземпляром класса Speaker.")

    def set_topic(self, topic):
        try:
            self.__topic = topic
        except ValueError:
            print("Тема должна быть строкой.")

    def add_slide(self, slide_content):
        try:
            self.__slides.append(slide_content)
            print(f"Добавлен слайд: {slide_content}")
        except ValueError:
            print("Содержание слайда должно быть строкой.")