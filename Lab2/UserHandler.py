import xml.sax


class UserHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.inUser = False
        self.currentUser = {}
        self.users = []
        self.term_number = None

    def startElement(self, name, attrs):
        if name == "user":
            self.inUser = True
            self.currentUser = dict(attrs)
        elif name == "term":
            # Обработка элемента term
            term_number = attrs.get("number")
            if term_number:
                self.term_number = term_number

    def characters(self, content):
        if self.inUser:
            # Заполнение значений элементов term
            if content.strip():
                self.currentUser[f"term{self.term_number}"] = content.strip()

    def endElement(self, name):
        if name == "user":
            self.inUser = False
            self.users.append(self.currentUser)
        elif name == "term":
            # Завершение обработки элемента term
            self.term_number = None


# parser = xml.sax.make_parser()
# handler = UserHandler()
# parser.setContentHandler(handler)
#
# with open('data/first.xml', 'r') as file:
#     parser.parse(file)
#
# # Выводим результат
# for user in handler.users:
#     print(user)
