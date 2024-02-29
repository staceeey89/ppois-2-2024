class Montage:
    def __init__(self):
        self._shot_list = []
        self._load_number = 0

    def get_shot_list(self):
        return self._shot_list

    def add_shot(self, shot):
        self._shot_list.append(shot)

    def increase_load_number(self):
        self._load_number += 1

    def get_load_number(self):
        return self._load_number
