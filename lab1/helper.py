import social_network as social_network_module
import gender as gender_module
import user as user_module
import news as news_module
import image as image_module
import message as message_module
import group as group_module
import exceptions
import datetime
import pickle


def find_user_by_username(social_network: social_network_module.SocialNetwork, username: str):
    for user in social_network.users:
        if user.username == username:
            return user
    return None


def find_group_by_name(social_network: social_network_module.SocialNetwork, name: str):
    for group in social_network.groups:
        if group.name == name:
            return group
    return None


def is_username_free(social_network: social_network_module.SocialNetwork, username: str):
    for user in social_network.users:
        if user.username == username:
            return False

    return True


def is_group_name_free(social_network: social_network_module.SocialNetwork, username: str):
    for group in social_network.groups:
        if group.name == username:
            return False

    return True


def menu_add_user(social_network: social_network_module.SocialNetwork):
    list_of_users = social_network.users

    username = input("Введите псевдоним пользователя: ")

    while not is_username_free(social_network, username):
        print("Данный псевдоним уже занят!\n")
        username = input("Введите псевдоним пользователя: ")

    name = input("Введите имя пользователя: ")
    surname = input("Введите фамилию пользователя: ")
    age = int(input("Введите возраст пользователя: "))
    gender = gender_module.Gender.from_string(input("Введите пол пользователя(мужской/женский): "))

    new_user = user_module.User(username, name, surname, age, gender, social_network)
    social_network.add_user(new_user)

    print("Пользователь успешно создан!")

    with open("resources/data.pickle", "wb") as file:
        pickle.dump(social_network, file)


def menu_add_news(social_network: social_network_module.SocialNetwork):
    username = input("Введите псевдоним пользователя, который будет публиковать новость: ")
    user = find_user_by_username(social_network, username)
    while user is None:
        print("Вы ввели несуществующий псевдоним пользователя!")
        username = input("Введите псевдоним пользователя, который будет публиковать новость: ")
        user = find_user_by_username(social_network, username)

    news_content = input("Введите контент новости: ")
    news_image_choose = int(input("Хотите ли вы добавить картинку к новости?(1 - да, 2 - нет): "))
    image = None
    if news_image_choose == 1:
        image_content = input("Введите контент изображения: ")
        image_height = int(input("Введите высоту изображения: "))
        image_width = int(input("Введите ширину изображения: "))
        image = image_module.Image(image_width, image_height, image_content)
    news = news_module.News(datetime.datetime.now(), news_content, image, user)
    user.post_news(news)

    print("Новость успешно опубликована!")

    with open("resources/data.pickle", "wb") as file:
        pickle.dump(social_network, file)


def menu_show_users(social_network: social_network_module.SocialNetwork):
    print(social_network.show_users())


def menu_show_news(social_network: social_network_module.SocialNetwork):
    print(social_network.show_newsline())


def menu_write_message(social_network: social_network_module.SocialNetwork):
    from_user_username = input("Введите псевдоним отправляющего: ")
    from_user = find_user_by_username(social_network, from_user_username)
    while from_user is None:
        print("Вы ввели несуществующий псевдоним пользователя!")
        from_user_username = input("Введите псевдоним отправляющего: ")
        from_user = find_user_by_username(social_network, from_user_username)

    to_user_username = input("Введите псевдоним получающего: ")
    to_user = find_user_by_username(social_network, to_user_username)
    while to_user is None:
        print("Вы ввели несуществующий псевдоним пользователя!")
        to_user_username = input("Введите псевдоним отправляющего: ")
        to_user = find_user_by_username(social_network, to_user_username)

    content = input("Введите сообщение: ")
    message = message_module.Message(from_user, to_user, content)
    from_user.write_message(message)

    print("Сообщение успешно отправлено!")

    with open("resources/data.pickle", "wb") as file:
        pickle.dump(social_network, file)


def menu_show_messages(social_network: social_network_module.SocialNetwork):
    username = input("Введите псевдоним пользователя, у которого хотели бы просмотреть сообщения: ")
    user = find_user_by_username(social_network, username)
    while user is None:
        print("Вы ввели несуществующий псевдоним пользователя!")
        username = input("Введите псевдоним пользователя, у которого хотели бы просмотреть сообщения: ")
        user = find_user_by_username(social_network, username)

    print("Отправленные сообщения: ")
    print(social_network.show_sent_messages(user))

    print("Полученные сообщения: ")
    print(social_network.show_received_massages(user))


def menu_add_group(social_network: social_network_module.SocialNetwork):
    name = input("Введите название группы: ")
    while not is_group_name_free(social_network, name):
        print("Данное имя группы уже существует!")
        name = input("Введите название группы: ")
    group = group_module.Group(name)
    social_network.add_group(group)

    print("Группа успешно создана!")

    with open("resources/data.pickle", "wb") as file:
        pickle.dump(social_network, file)


def menu_show_groups(social_network: social_network_module.SocialNetwork):
    print(social_network.show_groups())


def menu_add_user_to_group(social_network: social_network_module.SocialNetwork):
    username = input("Введите псевдоним пользователя: ")
    user = find_user_by_username(social_network, username)
    while user is None:
        print("Вы ввели несуществующий псевдоним пользователя!")
        username = input("Введите псевдоним пользователя: ")
        user = find_user_by_username(social_network, username)

    group_name = input("Введите название группы: ")
    group = find_group_by_name(social_network, group_name)
    while group is None:
        print("Вы ввели несуществующую группу!")
        group_name = input("Введите название группы: ")
        user = find_group_by_name(social_network, group_name)

    user.join_group(group)

    print("Пользователь успешно добавлен в группу!")

    with open("resources/data.pickle", "wb") as file:
        pickle.dump(social_network, file)


def menu_add_friend(social_network: social_network_module.SocialNetwork):
    username = input("Введите псевдоним пользователя: ")
    user = find_user_by_username(social_network, username)
    while user is None:
        print("Вы ввели несуществующий псевдоним пользователя!")
        username = input("Введите псевдоним пользователя: ")
        user = find_user_by_username(social_network, username)

    friend_username = input("Введите псевдоним друга: ")
    friend = find_user_by_username(social_network, friend_username)
    while friend is None:
        print("Вы ввели несуществующий псевдоним друга!")
        friend_username = input("Введите псевдоним друга: ")
        friend = find_user_by_username(social_network, friend_username)

    user.add_friend(friend)

    print("Друг успешно добавлен!")

    with open("resources/data.pickle", "wb") as file:
        pickle.dump(social_network, file)


def menu_delete_friend(social_network: social_network_module.SocialNetwork):
    username = input("Введите псевдоним пользователя: ")
    user = find_user_by_username(social_network, username)
    while user is None:
        print("Вы ввели несуществующий псевдоним пользователя!")
        username = input("Введите псевдоним пользователя: ")
        user = find_user_by_username(social_network, username)

    friend_username = input("Введите псевдоним друга: ")
    while is_username_free(social_network, friend_username):
        print("Вы ввели несуществующий псевдоним друга!")
        friend_username = input("Введите псевдоним друга: ")

    user.delete_friend(friend_username)

    print("Друг успешно удален!")

    with open("resources/data.pickle", "wb") as file:
        pickle.dump(social_network, file)
