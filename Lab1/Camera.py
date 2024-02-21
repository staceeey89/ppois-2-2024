class Camera:
    def __init__(self):
        self._hor_turn = 0
        self._vert_turn = 0
        self._message = None

    def turn_right(self, montage):
        if self._hor_turn < 1:
            self._hor_turn += 1
            self._message = "Камера повернута вправо."
            montage.add_shot(self._message)
            print(self._message)
            return True
        else:
            print("Камера не может больше повернуться вправо.")
            self._message = None
            return False

    def turn_left(self, montage):
        if self._hor_turn > -1:
            self._hor_turn -= 1
            self._message = "Камера повернута влево."
            montage.add_shot(self._message)
            print(self._message)
            return True
        else:
            print("Камера не может больше повернуться влево.")
            self._message = None
            return False

    def turn_up(self, montage):
        if self._vert_turn < 1:
            self._vert_turn += 1
            self._message = "Камера повернута вверх."
            montage.add_shot(self._message)
            print(self._message)
            return True
        else:
            print("Камера не может больше повернуться вверх.")
            self._message = None
            return False

    def turn_down(self, montage):
        if self._vert_turn > -1:
            self._vert_turn -= 1
            self._message = "Камера повернута вниз."
            montage.add_shot(self._message)
            print(self._message)
            return True
        else:
            print("Камера не может больше повернуться вниз.")
            self._message = None
            return False
