import datetime
import unittest

import user as user_module
import message as message_module
import group as group_module
import image as image_module
import news as news_module
import image as image_module
import message as message_module
import group as group_module
import newsline as newsline_module
import social_network as social_network_module
import gender as gender_module
import exceptions as exceptions_module


class TestUser(unittest.TestCase):
    def setUp(self):
        self.social_network = social_network_module.SocialNetwork("Facebook")
        self.first_user = user_module.User("megaaction", "Steve", "Jhonson", 19, gender_module.Gender.MALE,
                                           self.social_network)
        self.second_user = user_module.User("fiftycent", "Margaret", "Fitch", 27, gender_module.Gender.MALE,
                                            self.social_network)
        self.image = image_module.Image(500, 100, "Cats")
        self.message = message_module.Message(self.first_user, self.second_user, "Hello, how do you feel today?")
        self.news = news_module.News(datetime.datetime.now(), "Hi everyone! It is my cat!", self.image, self.first_user)
        self.group = group_module.Group("Cars")

    def test_add_friend(self):
        self.first_user.add_friend(self.second_user)
        self.assertEqual(self.first_user.friends[0], self.second_user)
        self.assertEqual(self.second_user.friends[0], self.first_user)

    def test_post_news(self):
        self.first_user.post_news(self.news)
        self.assertEqual(self.first_user.news[0], self.news)

    def test_write_message(self):
        self.first_user.write_message(self.message)
        self.assertEqual(self.first_user.sent_messages[0], self.message)
        self.assertEqual(self.second_user.received_messages[0], self.message)

    def test_join_group(self):
        self.first_user.join_group(self.group)
        self.assertEqual(self.first_user.groups[0], self.group)

    def test_delete_friends(self):
        self.first_user.add_friend(self.second_user)
        self.assertEqual(self.first_user.friends[0], self.second_user)
        self.assertEqual(self.second_user.friends[0], self.first_user)
        self.first_user.delete_friend(self.second_user.username)
        self.assertTrue(len(self.first_user.friends) == 0)
        self.assertTrue(len(self.second_user.friends) == 0)

    def test_user_with_exception(self):
        with self.assertRaises(exceptions_module.InvalidAgeValue):
            user = user_module.User("megaaction", "Steve", "Jhonson", -10, gender_module.Gender.MALE,
                                               self.social_network)

    def test_image_with_exception(self):
        with self.assertRaises(exceptions_module.InvalidResolutionValue):
            image = image_module.Image(-500, 100, "Cats")

    def test_gender_with_exception(self):
        with self.assertRaises(exceptions_module.InvalidGenderValue):
            gender = gender_module.Gender.from_string("мужскй")
