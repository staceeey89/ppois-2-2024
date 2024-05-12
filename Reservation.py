from Tables import Tables
from AbstractCustomer import AbstractCustomer

class Reservetion(Tables):
    
    def __init__(self, tablesDict: dict) -> None:
        super().__init__(tablesDict=tablesDict)  
    
    def takeTable(self, number, tables: Tables, customer: AbstractCustomer) -> bool:  
        if number in self._Tables__tablesDict:  
            if self._Tables__tablesDict[number] == "Reserved" or self._Tables__tablesDict[number] == "Occupied":
                print("Извините, этот столик занят")
                return False    
            else:
                print("Столик забронирован")
                self._Tables__tablesDict[number] = "Reserved"
                customer.tookTable()
                return True
        else:
            print("There is no table with such number")
            return False
