import unittest
from Television import *
from Remote_controle import *


class MyTestCase(unittest.TestCase):
    def test_tv_on(self):
        TV2 = Television('LG', '2500$', 'Grey')
        PULT2 = Remote_control('Samsung', '250$', 'Black', TV2)
        PULT2.turn_tv_on()
        self.assertTrue(TV2.is_on)
    def test_tv_off(self):
        TV2 = Television('LG', '2500$', 'Grey')
        PULT2 = Remote_control('Samsung', '250$', 'Black', TV2)
        self.assertFalse(PULT2.turn_tv_on())
    def test_channel(self):
        TV2 = Television('LG', '2500$', 'Grey')
        PULT2 = Remote_control('Samsung', '250$', 'Black', TV2)
        PULT2.turn_tv_on()
        PULT2.choose_new_channel('Entertainment')
        self.assertTrue(TV2._protected_check_channel())


if __name__ == '__main__':
    unittest.main()
