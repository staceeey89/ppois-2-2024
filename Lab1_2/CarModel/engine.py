from detail import Detail

class Engine(Detail):

    def __init__(self, volume: int, vendor: str, creation_year: int=2024, fuel_level: int =0, oil: bool=False):
        
        super().__init__(vendor, creation_year)
        self.__max_fuel_level: int = volume
        self.__fuel_level: int = fuel_level if fuel_level < volume else volume
        self.__oil: bool = oil
        self.__working: bool = False

    def __str__(self):

        return super().__str__()[:-1] + ", " + str({"Fuel level": self.__fuel_level, 
                                        "Max fuel level": self.__max_fuel_level, 
                                        "Oil": self.__oil})[1:]

    def get_max_fuel_level(self) -> int: return self.__max_fuel_level
    def get_fuel_level(self) -> int: return self.__fuel_level
    def maximize_fuel_level(self) -> None: self.__fuel_level = self.__max_fuel_level
    def is_oil(self) -> bool: return self.__oil
    def set_oil(self, state: bool): self.__oil = state 
    def change_working(self) -> None: self.__working = not self.__working
    def is_working(self) -> bool: return self.__working

    def fuel_waste(self) -> None:

        if self.__fuel_level: 
            self.__fuel_level -= 0.05 * self.__max_fuel_level
        else: print("Your gas tank is empty")
        

    
