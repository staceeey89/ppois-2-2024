class Document:
    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.signed = False

    def __str__(self):
        return self.name

    def fill_content(self, new_content):
        self.content = new_content

    def sign(self):
        self.signed = True
