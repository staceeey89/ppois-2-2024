import exception


class Room:
    def __init__(self, width: int, length: int):
        self.isClean: bool = False
        self.width: int = width
        self.length: int = length
        self.square: int = self.width*self.length

        if self.width <= 0 or self.length <= 0:
            raise exception.InvalidResolutionValue("‼ Введены неверные размеры комнаты")
