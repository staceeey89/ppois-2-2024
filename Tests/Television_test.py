import unittest
from Television import *


class MyTestCase(unittest.TestCase):
    def test_device(self):
        TV2 = Television("LG", "3400", "Green")
        self.assertTrue(TV2.device_connected('DVD Player', True))
    def test_update_softw(self):
        TV2 = Television("LG", "3400", "Green")
        TV2.set_software('webOS', '3.4')
        self.assertTrue(TV2.update_software('webOS', '3.92'))
    def test_add_britness(self):
        TV2 = Television("LG", "3400", "Green")
        self.assertEqual(TV2.add_britness(95), 95)
    def test_add_contrast(self):
        TV2 = Television("LG", "3400", "Green")
        self.assertEqual(TV2.add_contrast(80), 80)
    def test_add_saturationn(self):
        TV2 = Television("LG", "3400", "Green")
        self.assertEqual(TV2.add_saturation(43), 43)
        
if __name__ == '__main__':
    unittest.main()





