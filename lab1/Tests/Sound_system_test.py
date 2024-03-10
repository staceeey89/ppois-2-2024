import unittest
from Television import *
from Sound_system import *
from Remote_controle import *

class MyTestCase(unittest.TestCase):
    def test_check_sound1(self):
        TV2 = Television('LG', '2500$', 'Grey')
        self.assertFalse(TV2.change_sound_level(59))
    def test_check_sound2(self):
        TV2 = Television('LG', '2500$', 'Grey')
        PULT2 = Remote_control('Samsung', '250$', 'Black', TV2)
        PULT2.turn_tv_on()
        self.assertTrue(TV2.change_sound_level(59))


if __name__ == '__main__':
    unittest.main()
