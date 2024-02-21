import unittest
from Camera import Camera
from Montage import Montage


class CameraTestCase(unittest.TestCase):
    # Правый поворот
    def test_turn_right_success(self):
        montage = Montage()
        camera = Camera()
        result = camera.turn_right(montage)
        self.assertTrue(result)
        self.assertEqual(camera._hor_turn, 1)
        self.assertEqual(camera._message, "Камера повернута вправо.")
        self.assertEqual(len(montage.get_shot_list()), 1)
        self.assertEqual(montage.get_shot_list()[0], "Камера повернута вправо.")

    def test_turn_right_max_limit_reached(self):
        montage = Montage()
        camera = Camera()
        camera._hor_turn = 1
        result = camera.turn_right(montage)
        self.assertFalse(result)
        self.assertEqual(camera._hor_turn, 1)
        self.assertEqual(camera._message, None)
        self.assertEqual(len(montage.get_shot_list()), 0)

    # Левый поворот
    def test_turn_left_success(self):
        montage = Montage()
        camera = Camera()
        result = camera.turn_left(montage)
        self.assertTrue(result)
        self.assertEqual(camera._hor_turn, -1)
        self.assertEqual(camera._message, "Камера повернута влево.")
        self.assertEqual(len(montage.get_shot_list()), 1)
        self.assertEqual(montage.get_shot_list()[0], "Камера повернута влево.")

    def test_turn_left_max_limit_reached(self):
        montage = Montage()
        camera = Camera()
        camera._hor_turn = -1
        result = camera.turn_left(montage)
        self.assertFalse(result)
        self.assertEqual(camera._hor_turn, -1)
        self.assertEqual(camera._message, None)
        self.assertEqual(len(montage.get_shot_list()), 0)

    # Верхний поворот
    def test_turn_up_success(self):
        montage = Montage()
        camera = Camera()
        result = camera.turn_up(montage)
        self.assertTrue(result)
        self.assertEqual(camera._vert_turn, 1)
        self.assertEqual(camera._message, "Камера повернута вверх.")
        self.assertEqual(len(montage.get_shot_list()), 1)
        self.assertEqual(montage.get_shot_list()[0], "Камера повернута вверх.")

    def test_turn_up_max_limit_reached(self):
        montage = Montage()
        camera = Camera()
        camera._vert_turn = 1
        result = camera.turn_up(montage)
        self.assertFalse(result)
        self.assertEqual(camera._vert_turn, 1)
        self.assertEqual(camera._message, None)
        self.assertEqual(len(montage.get_shot_list()), 0)

    # Нижний поворот
    def test_turn_down_success(self):
        montage = Montage()
        camera = Camera()
        result = camera.turn_down(montage)
        self.assertTrue(result)
        self.assertEqual(camera._vert_turn, -1)
        self.assertEqual(camera._message, "Камера повернута вниз.")
        self.assertEqual(len(montage.get_shot_list()), 1)
        self.assertEqual(montage.get_shot_list()[0], "Камера повернута вниз.")

    def test_turn_down_max_limit_reached(self):
        montage = Montage()
        camera = Camera()
        camera._vert_turn = -1
        result = camera.turn_down(montage)
        self.assertFalse(result)
        self.assertEqual(camera._vert_turn, -1)
        self.assertEqual(camera._message, None)
        self.assertEqual(len(montage.get_shot_list()), 0)

