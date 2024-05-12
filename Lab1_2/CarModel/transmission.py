from detail import Detail
from carxceptions import SwitchAutomaticTransmissionError, InvalidGearError
import typegearsseason as tgs

class Transmission(Detail):
    
    def __init__(self, ttype: tgs.TransmissionType, 
                 vendor: str, creation_year: int=2024):

        super().__init__(vendor, creation_year)
        self.__type: tgs.TransmissionType = ttype

        if self.__type == tgs.TransmissionType.automatic:
            self.__gear: tgs.Gears = None
        else: self.__gear: tgs.Gears = tgs.Gears.N

    def __str__(self):
        return super().__str__()[:-1] + ", " + \
               str({"Type": self.__type.name,
                    "Current gear": self.__gear})[1:]

    def get_type(self) -> tgs.TransmissionType: return self.__type
    def get_gear(self): return self.__gear
    def set_gear(self, new_gear: tgs.Gears): 
        
        try:
            
            if new_gear not in tgs.Gears: raise InvalidGearError
            elif self.__type == tgs.TransmissionType.automatic: 
                raise SwitchAutomaticTransmissionError
            else: self.__gear = new_gear      
            
        except InvalidGearError: print("ERROR! This gear is not exist")
        except SwitchAutomaticTransmissionError:
             
            print("You dont need switch gear, " + 
                  "because your transmission is automatic")

