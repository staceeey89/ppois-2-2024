class Turnstile:
    def __init__(self):
        self.is_locked: bool = True

    def unlock(self) -> None:
        self.is_locked = False

    def lock(self) -> None:
        self.is_locked = True
