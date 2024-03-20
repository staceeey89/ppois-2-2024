import xml.dom.minidom as minidom
import xml.sax

from UserHandler import UserHandler

parser = xml.sax.make_parser()
handler = UserHandler()
parser.setContentHandler(handler)


class XML:
    def __init__(self):
        self.path = ""

    def set_connection(self, new_path=""):
        self.path = new_path

    def add_user_xml(self, first_name="", last_name="", patronymic="", user_group="", *terms):
        if first_name == "" or last_name == "" and patronymic == "" and user_group == "":
            return False
        try:
            with open(self.path, "r") as f:
                data = f.read()
                if len(data) > 0:
                    doc = minidom.parseString(data)
                else:
                    doc = minidom.Document()
        except FileNotFoundError:
            doc = minidom.Document()

        root = doc.firstChild
        if root is None:
            root = doc.createElement("users")
            doc.appendChild(root)

        user_exists = False
        users = doc.getElementsByTagName('user')
        for user in users:
            if (user.getAttribute("first_name") == first_name and
                    user.getAttribute("last_name") == last_name and
                    user.getAttribute("patronymic") == patronymic and
                    user.getAttribute("user_group") == user_group):
                print("User already exists")
                user_exists = True
                return False

        if not user_exists:
            student = doc.createElement("user")
            student.setAttribute("first_name", first_name)
            student.setAttribute("last_name", last_name)
            student.setAttribute("patronymic", patronymic)
            student.setAttribute("user_group", user_group)
            for i, term in enumerate(terms):
                term_element = doc.createElement("term")
                term_element.setAttribute("number", str(i + 1))
                term_element.appendChild(doc.createTextNode(str(term)))
                student.appendChild(term_element)
            root.appendChild(student)

        with open(self.path, "w") as f:
            f.write(doc.toprettyxml())
            return True

    def get_num_users(self):
        return len(handler.users)

    def get_users(self):
        return handler.users

    def update_users(self):
        handler.users.clear()
        with open(self.path, 'r') as file:
            parser.parse(file)

    def get_user_opt(self, num):
        opt = 0
        for i in range(4, 14):
            opt = sum([int(handler.users[num][f"term{i - 3}"]) for i in range(4, 14)])
        return opt

    # Поиск по группе и кол-ву работы
    def get_num_users_search_group_opt(self, group, low_opt, high_opt):
        # Вычисляет кол-во найденных людей
        counter = 0
        for user in handler.users:
            opt = sum([int(user[f"term{i - 3}"]) for i in range(4, 14)])
            if user["user_group"] == group and low_opt <= opt <= high_opt:
                counter += 1
        return counter

    def get_pos_users_group_opt(self, num, group, low_opt, high_opt, last_user):
        # Вычисляет, сколько людей нужно убрать в переходе на страницу
        need_num = num
        counter = 0
        us = handler.users
        flag = False
        for user in reversed(us):
            if user == last_user:
                flag = True
            if flag:
                if need_num <= 0:
                    return counter
                opt = sum([int(user[f"term{i - 3}"]) for i in range(4, 14)])
                if user["user_group"] == group and low_opt <= opt <= high_opt:
                    need_num -= 1
                counter += 1
        return counter

    # Поиск по фамилии и кол-ву работы
    def get_num_users_search_last_name_opt(self, last_name, low_opt, high_opt):
        # Вычисляет кол-во найденных людей
        counter = 0
        for user in handler.users:
            opt = sum([int(user[f"term{i - 3}"]) for i in range(4, 14)])
            if user["last_name"] == last_name and low_opt <= opt <= high_opt:
                counter += 1
        return counter

    def get_pos_users_last_name_opt(self, num, last_name, low_opt, high_opt, last_user):
        # Вычисляет, сколько людей нужно убрать в переходе на страницу
        need_num = num
        counter = 0
        us = handler.users
        flag = False
        for user in reversed(us):
            if user == last_user:
                flag = True
            if flag:
                if need_num <= 0:
                    return counter
                opt = sum([int(user[f"term{i - 3}"]) for i in range(4, 14)])
                if user["last_name"] == last_name and low_opt <= opt <= high_opt:
                    need_num -= 1
                counter += 1
        return counter

    # Поиск по фамилии и группе
    def get_num_users_search_last_name_group(self, last_name, group):
        # Вычисляет кол-во найденных людей
        counter = 0
        for user in handler.users:
            if user["last_name"] == last_name and user["user_group"] == group:
                counter += 1
        return counter

    def get_pos_users_last_name_group(self, num, last_name, group, last_user):
        # Вычисляет, сколько людей нужно убрать в переходе на страницу
        need_num = num
        counter = 0
        us = handler.users
        flag = False
        for user in reversed(us):
            if user == last_user:
                flag = True
            if flag:
                if need_num <= 0:
                    return counter
                if user["last_name"] == last_name and user["user_group"] == group:
                    need_num -= 1
                counter += 1
        return counter

    # Удаляет элемент по фамилии и группе
    def delete_users_last_name_group(self, last_name, user_group):
        # Загружаем XML-файл в документ
        doc = minidom.parse(self.path)

        # Находим элемент user по атрибутам last_name и user_group
        users = doc.getElementsByTagName("user")
        counter = 0
        for user in users:
            if user.getAttribute("last_name") == last_name and user.getAttribute("user_group") == user_group:
                # Удаляем элемент user
                user.parentNode.removeChild(user)
                counter += 1
        # Сохраняем изменения в XML-файл
        with open(self.path, "w") as f:
            f.write(doc.toxml())
        self.update_users()
        return counter

    # Удаляет все элементы по фамилии и кол-ву работы
    def delete_users_last_name_opt(self, last_name, low_opt, high_opt):
        doc = minidom.parse(self.path)
        users = doc.getElementsByTagName("user")
        counter = 0

        for user in users:
            total_sum = sum(int(term.firstChild.data) for term in user.getElementsByTagName("term"))
            if user.getAttribute("last_name") == last_name and low_opt <= total_sum <= high_opt:
                user.parentNode.removeChild(user)
                counter += 1
        with open(self.path, "w") as f:
            f.write(doc.toxml())
        self.update_users()
        return counter

    # Удаляет все элементы по группе и кол-ву работы
    def delete_users_group_opt(self, group, low_opt, high_opt):
        doc = minidom.parse(self.path)
        users = doc.getElementsByTagName("user")
        counter = 0

        for user in users:
            total_sum = sum(int(term.firstChild.data) for term in user.getElementsByTagName("term"))
            if user.getAttribute("user_group") == group and low_opt <= total_sum <= high_opt:
                user.parentNode.removeChild(user)
                counter += 1
        with open(self.path, "w") as f:
            f.write(doc.toxml())
        self.update_users()
        return counter

# xml = XML()
# xml.set_connection("data/first.xml")
# xml.update_users()
# print(len(handler.users))
# xml.delete_users_group_opt("111111", 1, 200)
# print(len(handler.users))
