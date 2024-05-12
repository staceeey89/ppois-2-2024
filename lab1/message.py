import user as user_module


class Message:
    def __init__(self, from_user: 'user_module.User', to_user: 'user_module.User', content: str):
        self.from_user: user_module.User = from_user
        self.to_user: user_module.User = to_user
        self.content: str = content

    def __str__(self):
        information = (f"💬{self.from_user.username} -> {self.to_user.username}\n"
                       f"Сообщение: {self.content}")

        return information
