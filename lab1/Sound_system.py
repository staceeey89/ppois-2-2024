class Sound_system:
    def __init__(self):
        self.sound_level: int = 0

    def change_sound_level(self, level: int):
        if self.sound_level < level:
            self.sound_level = level
            print(f'Sound level increased to {level}')
        elif self.sound_level > level:
            self.sound_level = level
            print(f'Sound level decreased to {level}')
        else:
            self.sound_level = level
            print(f'Sound level remains at level {level}')