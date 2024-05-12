import pickle
import os
import social_network as social_network_module
import helper
import os

if __name__ == '__main__':
    if not os.path.isfile("resources/data.pickle") or os.path.getsize("resources/data.pickle") == 0:
        name_of_social_network = input("Вы еще не создали социальную сеть!\n"
                                       "Введите название вашей социальной сети, чтобы ее создать: ")
        social_network = social_network_module.SocialNetwork(name_of_social_network)
        with open("resources/data.pickle", "wb") as file:
            pickle.dump(social_network, file)

    else:
        with open("resources/data.pickle", "rb") as file:
            social_network = pickle.load(file)
            print("Добро пожаловать в {}".format(social_network.name))

        menu_choose = int(input("1. Добавить пользователя.\n2. Добавить новость.\n3. Добавить друга.\n"
                                "4. Добавить группу.\n5. Добавить пользователя в группу."
                                "\n6. Просмотреть пользователей.\n7. Просмотреть новости.\n"
                                "8. Просмотреть сообщения.\n9. Просмотреть все группы.\n10. Написать сообщение.\n"
                                "11. Удалить друга.\nВведите ваш выбор: "))
        print()

        if menu_choose == 1:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_add_user(social_network)

        elif menu_choose == 2:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_add_news(social_network)

        elif menu_choose == 3:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_add_friend(social_network)

        elif menu_choose == 4:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_add_group(social_network)

        elif menu_choose == 5:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_add_user_to_group(social_network)

        elif menu_choose == 6:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_show_users(social_network)

        elif menu_choose == 7:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_show_news(social_network)

        elif menu_choose == 8:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_show_messages(social_network)

        elif menu_choose == 9:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_show_groups(social_network)

        elif menu_choose == 10:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_write_message(social_network)

        elif menu_choose == 11:
            os.system("clear")
            with open("resources/data.pickle", "rb") as file:
                social_network = pickle.load(file)
            helper.menu_delete_friend(social_network)
