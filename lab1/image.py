import exceptions


class Image:
    def __init__(self, width: int, height: int, content: str):
        self.width: int = width
        self.height: int = height
        self.content: str = content

        if self.width <= 0 or self.height <= 0:
            raise exceptions.InvalidResolutionValue("Введены неверные значения ")

    def __str__(self):
        information = (f"Контент картинки: {self.content}\nШирина картинки: {self.width}\n"
                       f"Высота картинки: {self.height}")

        return information
