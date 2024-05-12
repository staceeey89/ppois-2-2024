class RepositoryException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class ViewException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)