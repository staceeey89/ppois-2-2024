import group as group_module
import newsline as newsline_module
import user as user_module
import news as news_module
import message as message_module


class SocialNetwork:
    def __init__(self, name: str):
        self.name: str = name
        self.users: list = []
        self.groups: list = []
        self.messages: list = []
        self.newsline: newsline_module.Newsline = newsline_module.Newsline()

    def add_user(self, user: 'user_module.User'):
        self.users.append(user)

    def add_group(self, group: 'group_module.Group'):
        self.groups.append(group)

    def add_news(self, news: 'news_module.News'):
        self.newsline.add_news(news)

    def add_message(self, message: 'message_module.Message'):
        self.messages.append(message)

    def get_news(self):
        return self.newsline.news

    def show_newsline(self):
        return str(self.newsline)

    def show_users(self):
        information = ""
        for user in self.users:
            information += str(user) + "\n"

        return information

    def show_groups(self):
        information = ""
        for group in self.groups:
            information += str(group) + "\n"

        return information

    def show_received_massages(self, user: 'user_module.User'):
        information = ""
        if user in self.users:
            for message in user.received_messages:
                information += str(message) + "\n"

        return information

    def show_sent_messages(self, user: 'user_module.User'):
        information = ""
        if user in self.users:
            for message in user.sent_messages:
                information += str(message) + "\n"

        return information
