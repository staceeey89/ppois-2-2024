import datetime
import image as image_module
import user as user_module


class News:
    def __init__(self, date: datetime.datetime, content: str, image: image_module.Image, user: 'user_module.User'):
        self.image: image_module.Image = image
        self.date: datetime.datetime = date
        self.content: str = content
        self.user: user_module.User = user

    def __str__(self):
        information = (f"Дата публикации: {self.date}\nКонтент: {self.content}\n🌄Картинка:\n{self.image}\n"
                       f"Пользователь, который опубликовал: {self.user.username}\n")

        return information
