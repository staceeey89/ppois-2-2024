from abc import ABC, abstractmethod

class AbstractCustomer(ABC):
    @abstractmethod
    def madeOrder(self) -> None:
        pass
    
    def tookTable(self) -> None:
        pass
