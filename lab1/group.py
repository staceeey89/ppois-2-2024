import user as user_module


class Group:
    def __init__(self, name: str):
        self.name: str = name
        self.members: list = []

    def add_user(self, user: 'user_module.User'):
        self.members.append(user)

    def __str__(self):
        information = f"Название группы: {self.name}\nУчастники:\n"

        for member in self.members:
            information += member.username + "\n"

        return information
