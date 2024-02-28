from Television import *


class Technic_charact:
    def __init__(self, _screen_diagonal, _screen_resolution, _matrix_type):
        self._screen_diagonal: str = _screen_diagonal
        self._screen_resolution: str = _screen_resolution
        self._matrix_type: str = _matrix_type

    def print_data(self):
        print('Technical characteristics of TV:')
        print('Diagonal:', self._screen_diagonal, 'Screen resolution:', self._screen_resolution,  'Type of matrix:', self._matrix_type)