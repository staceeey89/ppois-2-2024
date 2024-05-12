class Pause:
    def __init__(self):
        self.duration = 0

    def stop(self, duration: int):
        self.duration = duration

    def frame(self):
        if self.duration >= 0:
            self.duration -= 1

    def __call__(self, *args, **kwargs):
        if self.duration >= 0:
            return True
        return False
