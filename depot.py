from typing import List
from abstractions import AbstractTrain


class Depot:
    def __init__(self):
        self.__trains: List[AbstractTrain] = []

    def pull_into(self, train: AbstractTrain):
        self.__trains.append(train)

    def pull_out_train(self):
        try:
            if len(self.__trains) != 0:
                return self.__trains.pop()
            else:
                raise IndexError("В депо нет поездов!")
        except IndexError as e:
            print(e)

    def get_trains_list(self):
        return self.__trains
