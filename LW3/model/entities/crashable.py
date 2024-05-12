from model.repository import load_sound


class Crashable():
    def __init__(self, crash_sound="crash", crash_callback=None):
        self.crash_sound = load_sound(crash_sound)
        self.crash_callback = crash_callback

    def crash(self):
        self.crash_sound.play()
        if self.crash_callback:
            self.crash_callback()
