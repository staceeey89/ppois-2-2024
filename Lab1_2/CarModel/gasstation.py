from typing import Generator
from adddel import AddDel
from car import Car


class GasStation(AddDel):

    __queue: set[Car] = set()

    @classmethod
    def get_queue(cls): return cls.__queue

    @classmethod
    def set_queue(cls, cars: set[Car]): cls.__queue = cars

    @classmethod
    def add(cls, car: Car): 
        
        if car not in cls.__queue:
            cls.__queue.add(car)
        else: print("Not added, because this car is already in queue")

    @classmethod
    def rem(cls, car: Car): 

        if car in cls.__queue:
            cls.__queue.remove(car)
        else: print("Nothing to delete, because this car is not in queue")

    @classmethod
    def gen_refueling_cars(cls) -> Generator:

        while cls.__queue:
            
            car = cls.__queue.pop()
            car.refueling()
            yield car
        

            
        