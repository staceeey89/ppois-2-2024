class Detail:

    def __init__(self, vendor: str, creation_year: int=2024):
        
        self._vendor: str = vendor
        self._creation_year: int = creation_year if (2024 >= creation_year >= 2014) else 2024
        self._state: int = -2014 + creation_year if (2024 >= creation_year >= 2014) else 0

    def __str__(self):
        
        return str({"Vendor": self._vendor, "Creation year": self._creation_year, 
                    "State": self._state})

    def get_vendor(self) -> str: return self._vendor
    def get_creation_year(self) -> int: return self._creation_year
    def get_state(self) -> int: return self._state
    def restore(self): self._state = 10
    def damage(self): self._state -= 1

    
        
        
            
        

    
