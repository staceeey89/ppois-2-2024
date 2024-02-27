from Television import *
class Technic_charact:
    def __init__(self, screen_diagonal, screen_resolution, matrix_type):
        self.screen_diagonal: str = screen_diagonal
        self.screen_resolution: str = screen_resolution
        self.matrix_type: str = matrix_type

    def print_data(self):
        print('Technical characteristics of TV:')
        print('Diagonal:', self.screen_diagonal, 'Screen resolution:', self.screen_resolution,  'Type of matrix:', self.matrix_type)