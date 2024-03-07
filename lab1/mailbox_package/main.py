from mailbox_package.mailbox import Sender
from mailbox_package.mailbox import Receiver
from mailbox_package.mailbox import Mailbox
# from mailbox_package.mailbox import set_local_mailbox
# from mailbox_package.mailbox import get_local_mailbox
# from mailbox_package.mailbox import local_mailbox
from time import sleep
from random import randint
# import pickle


def indent() -> None:
    print("-" * 80)


def show_senders() -> None:
    print("Senders:")
    print("1. Bob")
    print("2. Caleb")
    print("3. Alex")
    print("4. Nova")
    print("5. Vera")


def show_receivers() -> None:
    print("Receivers:")
    print("1. Mya")
    print("2. Peter")
    print("3. Robert")
    print("4. Emma")
    print("5. Lana")


def write_mail_menu(sender: Sender) -> None:
    show_receivers()
    chosen_receiver = input("Choose your receiver: ")
    indent()
    match chosen_receiver:
        case "1":
            sender.write_a_mail(mya, input("Enter any content to send: "))
        case "2":
            sender.write_a_mail(peter, input("Enter any content to send: "))
        case "3":
            sender.write_a_mail(robert, input("Enter any content to send: "))
        case "4":
            sender.write_a_mail(emma, input("Enter any content to send: "))
        case "5":
            sender.write_a_mail(lana, input("Enter any content to send: "))
        case _:
            print("Invalid receiver.")


def receiver_interaction_menu(receiver: Receiver) -> None:
    indent()
    print(f"You choose {receiver.name}. Receiver interaction menu:")
    print("1. Check notifications.")
    print("2. Delete all notifications.")
    print("3. Take the mail.")
    print("4. Check received mails.")
    print("5. Burn all receiver mails")
    print("If you enter an invalid input, you will be forwarded to the menu.")
    chosen_receiver_operation: str = input("Enter your receiver operation: ")
    indent()
    match chosen_receiver_operation:
        case "1":
            receiver.check_notifications()
        case "2":
            receiver.delete_all_notifications()
        case "3":
            receiver.take_the_letter()
        case "4":
            receiver.check_received_mails()
        case "5":
            receiver.burn_the_mails()
        case _:
            print("Invalid receiver operation.")


def receiver_menu() -> None:
    indent()
    show_receivers()
    print("If you enter an invalid input, you will be forwarded to the menu.")
    chosen_receiver: str = input("Enter your receiver: ")
    match chosen_receiver:
        case "1":
            receiver_interaction_menu(mya)
        case "2":
            receiver_interaction_menu(peter)
        case "3":
            receiver_interaction_menu(robert)
        case "4":
            receiver_interaction_menu(emma)
        case "5":
            receiver_interaction_menu(lana)
        case _:
            print("Invalid receiver.")


def sender_interaction_menu(sender: Sender) -> None:
    indent()
    print(f"You choose {sender.name}. Sender interaction menu:")
    print("1. Write a mail.")
    print("2. Check all mails.")
    print("3. Send all mails.")
    print("If you enter an invalid input, you will be forwarded to the menu.")
    chosen_sender_operation: str = input("Enter your sender operation: ")
    indent()
    match chosen_sender_operation:
        case "1":
            write_mail_menu(sender)
        case "2":
            sender.check_mail()
        case "3":
            sender.send_all_mails()
        case _:
            print("Invalid sender operation.")


def sender_menu() -> None:
    indent()
    show_senders()
    print("If you enter an invalid input, you will be forwarded to the menu.")
    chosen_sender: str = input("Enter your sender: ")
    match chosen_sender:
        case "1":
            sender_interaction_menu(bob)
        case "2":
            sender_interaction_menu(caleb)
        case "3":
            sender_interaction_menu(alex)
        case "4":
            sender_interaction_menu(nova)
        case "5":
            sender_interaction_menu(vera)
        case _:
            print("Invalid sender.")


def check_local_mailbox_condition() -> None:
    indent()
    print("Checking mailbox condition...")
    failure_rate: int = randint(1, 10)
    if failure_rate == 1:
        print("The mailbox accidentally broke. Repairs needed.")
        print("Repairmen are on their way...")
        sleep(5)
        print("The repairmen are getting to work...")
        sleep(5)
        print("Almost done...")
        sleep(5)
        print("The box has been successfully repaired.")
    else:
        print("The mailbox works normally.")


def menu() -> None:
    # set_local_mailbox(Mailbox(10))
    while True:
        indent()
        print("Main menu:")
        print("1. Choose a sender.")
        print("2. Choose a receiver.")
        print("3. Check mailbox condition.")
        print("0. Exit.")
        print("If you enter an invalid input, you will be forwarded to the menu.")
        choice: str = input("Enter you choice: ")
        match choice:
            case "1":
                sender_menu()
            case "2":
                receiver_menu()
            case "3":
                check_local_mailbox_condition()
            # case "4":
            #     with open("mailbox.pickle", "wb") as file:
            #         pickle.dump(get_local_mailbox(), file)
            # case "5":
            #     with open("mailbox.pickle", "rb") as file:
            #         mailbox: Mailbox = pickle.load(file)
            #         local_mailbox = mailbox
            #         # set_local_mailbox(mailbox)
            case "0":
                print("Exiting...")
                exit()
            case _:
                print("Invalid choice.")


if __name__ == '__main__':
    bob: Sender = Sender("Bob")
    caleb: Sender = Sender("Caleb")
    alex: Sender = Sender("Alex")
    nova: Sender = Sender("Nova")
    vera: Sender = Sender("Vera")
    mya: Receiver = Receiver("Mya")
    peter: Receiver = Receiver("Peter")
    robert: Receiver = Receiver("Robert")
    emma: Receiver = Receiver("Emma")
    lana: Receiver = Receiver("Lana")
    menu()
