from attraction import Attraction


class Photo:
    def __init__(self, attraction: Attraction, height: int, width: int, beautiful_level: int):

        if height <= 0 or width <= 0:
            raise ValueError("Negative size")

        self.attraction = attraction
        self.height = height
        self.width = width
        self.beautiful_level = beautiful_level

    def browsing_photo(self):
        return self.attraction
