from AbstractCustomer import AbstractCustomer

class Tables:
    
    def __init__(self, tablesDict: dict) -> None:
        self.__tablesDict = tablesDict
    
    def getInfo(self) -> str:
        for number, condition in self.__tablesDict.items():
            print(f"{number} - {condition}")
            
    def takeTable(self, number: int, customer: AbstractCustomer) -> bool:
        if number in self.__tablesDict:
            if self.__tablesDict[number] == "Reserved" or self.__tablesDict[number] == "Occupied":
                print("Извините, этот столик занят")
                return False
            else:
                print("Присаживайтесь")
                self.__tablesDict[number] = "Occupied"
                customer.tookTable()
                return True
        else:
            print("There is no table with such number")
            return False
            