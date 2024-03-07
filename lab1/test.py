import unittest
from mailbox_package.mailbox import *


class TestMail(unittest.TestCase):
    def test_mail(self):
        mail: Mail = Mail(
            Sender("Tom"),
            Receiver("Mak"),
            "Good evening"
        )
        self.assertEqual(str(mail.sender), "Tom")
        self.assertEqual(str(mail.receiver), "Mak")
        self.assertEqual(mail.content, "Good evening")

    def test_received_mail(self):
        tom: Sender = Sender("Tom")
        mak: Receiver = Receiver("Mak")
        tom.write_a_mail(mak, "Hi")
        tom.send_all_mails()
        mak.check_notifications()
        mak.delete_all_notifications()
        self.assertEqual(len(local_mailbox.lockers), 10)

    def test_received_mail2(self):
        tom: Sender = Sender("Tom")
        mak: Receiver = Receiver("Mak")
        tom.write_a_mail(mak, "Hi")
        mail: Mail = tom.mails.pop()
        self.assertEqual(str(mail), "Tom -> Mak: Hi")


class TestNotification(unittest.TestCase):
    def test_notification(self):
        sender: Sender = Sender("Max")
        receiver: Receiver = Receiver("Tom")
        locker_number = randint(1, 10)
        password: int = randint(1, 9999)
        notification: Notification = Notification(sender, receiver, locker_number, password)

        self.assertEqual(str(notification.sender), "Max")
        self.assertEqual(str(notification.receiver), "Tom")
        self.assertEqual(notification.locker, locker_number)
        self.assertEqual(notification.password, password)

    def test_number_of_notifications(self):
        self.assertEqual(local_mailbox.mailbox_capacity, 10)
        tom: Sender = Sender("Tom")
        mak: Receiver = Receiver("Mak")
        tom.write_a_mail(mak, "Hi")
        self.assertEqual(local_mailbox.current_capacity, 10)
        self.assertEqual(len(mak.notifications), 0)
        mak.check_notifications()
        mak.delete_all_notifications()
        tom.send_all_mails()
        self.assertEqual(len(mak.notifications), 0)
        mak.check_notifications()
        mak.delete_all_notifications()
        self.assertEqual(len(mak.notifications), 0)

    def test_notification2(self):
        tom: Sender = Sender("Tom")
        mak: Receiver = Receiver("Mak")
        tom.write_a_mail(mak, "Hi")
        tom.send_all_mails()

    def test_str_notification(self):
        tim: Sender = Sender("Tom")
        miko: Receiver = Receiver("Mak")
        miko.check_notifications()
        miko.delete_all_notifications()
        miko.check_notifications()
        tim.write_a_mail(miko, "Hi")
        miko.check_notifications()
        tim.send_all_mails()
        miko.check_notifications()
        miko.delete_all_notifications()


class TestMailbox(unittest.TestCase):
    def test_all_lockers_full(self):
        tom: Sender = Sender("Tom")
        mak: Receiver = Receiver("Mak")
        local_mailbox._protected_check_lockers()
        local_mailbox._protected_check_storage()
        for _ in range(11):
            tom.write_a_mail(mak, "")
        tom.send_all_mails()
        self.assertEqual(len(local_mailbox.lockers), 10)
        self.assertEqual(len(local_mailbox.storage), 2)
        local_mailbox._protected_check_lockers()
        local_mailbox._protected_check_storage()


class TestReceiver(unittest.TestCase):
    def test_take_the_letter(self):
        local_mailbox._protected_clear_lockers()
        x: Sender = Sender("X")
        self.assertEqual(len(x.mails), 0)
        y: Receiver = Receiver("Y")
        y.check_notifications()
        y.burn_the_mails()
        x.check_mail()
        x.write_a_mail(y, "Hi y")
        self.assertEqual(len(x.mails), 1)
        x.check_mail()
        x.send_all_mails()
        x.check_mail()
        self.assertEqual(len(x.mails), 0)
        y.check_received_mails()
        y.check_notifications()
        y.take_the_letter()
        y.take_the_letter()
        y.check_received_mails()
        y.burn_the_mails()

