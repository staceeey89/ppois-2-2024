import news as news_module


class Newsline:
    def __init__(self):
        self.news: list = []

    def add_news(self, news: news_module.News):
        self.news.append(news)

    def __str__(self):
        information = ""

        for news in self.news:
            information += str(news) + "\n"

        return information
