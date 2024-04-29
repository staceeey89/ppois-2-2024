import typegearsseason as tgs
from detail import Detail

class Wheels(Detail):
    
    def __init__(self, season: tgs.Season, vendor: str, creation_year: int=2024):

        super().__init__(vendor, creation_year)
        self.__season: tgs.Season = season

    def __str__(self):
        return super().__str__()[:-1] + ", " + str({"Season": self.__season.name})[1:]
        
    def get_season(self) -> tgs.Season: return self.__season