import gender as gender_module
import social_network as social_network_module
import message as message_module
import news as news_module
import group as group_module
import exceptions


class User:
    def __init__(self, username: str, name: str, surname: str, age: int, gender: 'gender_module.Gender',
                 social_network: 'social_network_module.SocialNetwork'):
        self.username: str = username
        self.name: str = name
        self.surname: str = surname
        self.age: int = age
        self.gender: gender_module.Gender = gender
        self.social_network: social_network_module.SocialNetwork = social_network
        self.friends: list = []
        self.news: list = []
        self.sent_messages: list = []
        self.received_messages: list = []
        self.groups: list = []

        if self.age < 0:
            raise exceptions.InvalidAgeValue("Вы ввели неверное значение для возраста!")

    def add_friend(self, friend: 'User'):
        self.friends.append(friend)
        friend.friends.append(self)

    def delete_friend(self, username: str):
        for friend in self.friends:
            if friend.username == username:
                self.friends.remove(friend)
                friend.friends.remove(self)

    def post_news(self, news: news_module.News):
        self.news.append(news)
        self.social_network.add_news(news)
        news.user = self

    def write_message(self, message: message_module.Message):
        self.social_network.add_message(message)
        self.sent_messages.append(message)
        message.to_user.received_messages.append(message)

    def join_group(self, group: 'group_module.Group'):
        self.groups.append(group)
        group.add_user(self)

    def __str__(self):
        information = (f"👤Псевдоним пользователя: {self.username}\nИмя пользователя {self.name}\n"
                       f"Фамилия пользователя: {self.surname}\nВозраст пользователя: {self.age}\n"
                       f"Пол пользователя: {self.gender.value}\n📷Новости пользователя:\n")
        for news in self.news:
            information += str(news)

        information += "👥Группы пользователя:\n"
        for group in self.groups:
            information += str(group)

        information += "👬Друзья пользователя:\n"
        for friend in self.friends:
            information += friend.username

        information += "\n"

        return information
