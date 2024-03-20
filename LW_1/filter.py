class Filter:
    def __init__(self):
        self.health: int = 5

    def usage_of_filter(self):
        self.health -= 1

    def renew_filter(self):
        self.health = 5
        print("Фильтр был заменён.")
