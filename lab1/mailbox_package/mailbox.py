from random import randint
from typing import List


class Mail:
    def __init__(self, sender, receiver, content) -> None:
        self.sender: Sender = sender
        self.receiver: Receiver = receiver
        self.content: str = content

    def __str__(self) -> str:
        return f'{self.sender} -> {self.receiver}: {self.content}'


class Mailbox:
    def __init__(self, _mailbox_capacity: int) -> None:
        self._mailbox_capacity: int = _mailbox_capacity
        self._current_capacity: int = 0
        self._lockers: List[dict | None] = [None] * _mailbox_capacity
        self._storage: List[Mail] = []

    def add_mail(self, mail) -> None:
        if self._current_capacity == self._mailbox_capacity:
            print("All lockers are full, adding mail to the storage.")
            self._storage.append(mail)
        else:
            password: int = randint(0, 9999)
            for i in range(len(self._lockers)):
                if self._lockers[i] is None:
                    self._lockers[i] = {password: mail}
                    notification: Notification = Notification(mail.sender,
                                                              mail.receiver, self._current_capacity,
                                                              password)
                    mail.receiver.add_notification(notification)
                    self._current_capacity += 1
                    break

    def _protected_check_lockers(self) -> None:
        print("Lockers:")
        for i in range(len(self._lockers)):
            if self._lockers[i] is None:
                print("Empty locker.")
            else:
                print("Password: ", *self._lockers[i],
                      ". Mail: ", *self._lockers[i].values(), sep='')

    def _protected_check_storage(self) -> None:
        if len(self._storage) == 0:
            print("Storage is empty.")
        else:
            print("Storage:")
            for i in range(len(self._storage)):
                print(self._storage[i])

    def _protected_clear_lockers(self) -> None:
        for i in range(len(self._lockers)):
            if self._lockers[i] is not None:
                self._lockers[i] = None
        self._current_capacity = 0
        for _ in range(min(len(self._storage), self._current_capacity)):
            self.add_mail(self._storage.pop())

    @property
    def lockers(self):
        return self._lockers

    @property
    def storage(self):
        return self._storage

    @property
    def current_capacity(self):
        return self._current_capacity

    @current_capacity.setter
    def current_capacity(self, value):
        self._current_capacity = value

    @property
    def mailbox_capacity(self):
        return self._mailbox_capacity


# def set_local_mailbox(mailbox: Mailbox) -> Mailbox:
#     return mailbox
#
#
# def get_local_mailbox() -> Mailbox:
#     return local_mailbox


local_mailbox: Mailbox = Mailbox(10)


class Notification:
    def __init__(self, sender, receiver, locker, password) -> None:
        self.sender: Sender = sender
        self.receiver: Receiver = receiver
        self.locker: int = locker
        self.password: int = password

    def __str__(self) -> str:
        return (f"{self.receiver}, you have a new mail from {self.sender}. "
                f"Locker: {self.locker + 1}, password: {self.password}")


class Receiver:
    def __init__(self, name) -> None:
        self.name: str = name
        self.notifications: List[Notification] = []
        self.received_mails: List[Mail] = []

    def __str__(self) -> str:
        return f'{self.name}'

    def add_notification(self, notification) -> None:
        self.notifications.append(notification)

    def check_notifications(self) -> None:
        if len(self.notifications) == 0:
            print(f"{self.name} don't have any notification.")
        else:
            print(f"{self.name}'s notifications:")
            for notification in self.notifications:
                print(notification)

    def delete_all_notifications(self) -> None:
        if len(self.notifications) == 0:
            print(f"{self.name} don't have any notification.")
        else:
            print(f"{self.name} deleted all the notifications.")
            self.notifications.clear()

    def take_the_letter(self) -> None:
        while True:
            locker_number: str | int = input("Enter your locker number: ")
            if locker_number.isnumeric():
                locker_number = int(locker_number) - 1
                if 0 <= locker_number <= local_mailbox.mailbox_capacity:
                    print("This locker is locked.")
                    break

        if local_mailbox.lockers[locker_number] is None:
            print("This locker is empty.")
        else:
            for _ in range(3):
                while True:
                    locker_password: str | int = input("Enter your locker number: ")
                    if locker_password.isnumeric():
                        locker_password = int(locker_password)
                        if 0 <= locker_password <= 9999:
                            break
                    print("Invalid password.")
                if locker_password not in local_mailbox.lockers[locker_number].keys():
                    print("This password is incorrect.")
                else:
                    print(f"{self.name} got a mail.")
                    self.received_mails.append(
                        local_mailbox.lockers[locker_number].pop(locker_password))
                    local_mailbox.lockers[locker_number] = None
                    local_mailbox.current_capacity -= 1
                    if len(local_mailbox.storage) != 0:
                        local_mailbox.add_mail(local_mailbox.storage.pop())
                    break
            else:
                print(f"{self.name} don't think (s)he know the password.")

    def check_received_mails(self) -> None:
        if len(self.received_mails) == 0:
            print(f"Nobody's texted {self.name} yet 😭")
        else:
            for mail in self.received_mails:
                print(mail)

    def burn_the_mails(self) -> None:
        if len(self.received_mails) == 0:
            print(f"Oh, {self.name} don't have any mails.")
        else:
            print(f"{self.name} is feeling warm 🔥.")
            self.received_mails.clear()


class Sender:
    def __init__(self, name) -> None:
        self.name: str = name
        self.mails: List[Mail] = []

    def __str__(self) -> str:
        return f'{self.name}'

    def write_a_mail(self, receiver, content) -> None:
        print(f"{self.name} wrote a mail to {receiver}")
        mail: Mail = Mail(self, receiver, content)
        self.mails.append(mail)

    def check_mail(self) -> None:
        if len(self.mails) == 0:
            print(f"{self.name} haven't wrote any mail yet.")
        else:
            print(f"{self.name} have some mails here:")
            for mail in self.mails:
                print(mail)

    def send_all_mails(self) -> None:
        if len(self.mails) == 0:
            print(f"{self.name} haven't wrote any mail yet.")
        else:
            print(f"{self.name} is sending mails...")
            for _ in range(len(self.mails)):
                mail: Mail = self.mails.pop()
                print(f"{self.name} sending mail to {mail.receiver}")
                local_mailbox.add_mail(mail)
            print("All mails sent.")


# if __name__ == '__main__':
#     local_mailbox = set_local_mailbox(Mailbox(10))
