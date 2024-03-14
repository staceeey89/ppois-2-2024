from typing import List
from station import Station
from train import Train
from datetime import timedelta
from depot import Depot


class Schedule:
    def __init__(self):
        self.__stations: List[Station] = []
        self.__trains: List[Train] = []
        self.__depots: List[Depot] = []
        self.__start_time: timedelta = timedelta(hours=5, minutes=30)
        self.__end_time: timedelta = timedelta(hours=00, minutes=40)
        self.__delta_time: timedelta = timedelta(minutes=0)
        self.__trains_counter: int = 0

    def add_train(self, train: Train):
        try:
            if len(self.__stations) >= len(self.__trains):
                self.__trains.append(train)
            else:
                Exception("Subway is overfilled by trains!")
        except Exception as text:
            print(text)

    def fill_depots(self):
        flag: bool = False
        for train in self.__trains:
            if flag is False:
                self.__depots[0].pull_into(train)
                flag = True
            else:
                self.__depots[1].pull_into(train)
                flag = False

    def remove_train(self, train: Train):
        self.__trains.remove(train)

    def add_station(self, station: Station):
        self.__stations.append(station)

    def remove_station(self, station: Station):
        self.__stations.remove(station)

    def set_time_delay(self):
        if timedelta(hours=5, minutes=30) <= self.__start_time <= timedelta(hours=7):
            self.__delta_time = timedelta(minutes=7)
            return
        if timedelta(hours=7) <= self.__start_time <= timedelta(hours=9):
            self.__delta_time = timedelta(minutes=2)
            return
        if timedelta(hours=9) <= self.__start_time <= timedelta(hours=16):
            self.__delta_time = timedelta(minutes=5)
            return
        if timedelta(hours=16) <= self.__start_time <= timedelta(hours=19):
            self.__delta_time = timedelta(minutes=3)
            return
        if timedelta(hours=19) <= self.__start_time <= timedelta(hours=21):
            self.__delta_time = timedelta(minutes=5)
            return
        if timedelta(hours=21) <= self.__start_time <= self.__end_time:
            self.__delta_time = timedelta(minutes=11)
            return

    def print_info(self):
        print(f"It is {self.__start_time}\nNearest train will be in {self.__delta_time}")

    def run_a_train(self):
        try:
            if len(self.__depots[0].get_trains_list()) == 0 and len(self.__depots[1].get_trains_list()) == 0:
                Exception("Depots are empty")
            if self.__stations[0].get_platforms()[0].train is None:
                self.__stations[0].get_platforms()[0].train = self.__depots[0].pull_out_train()
                self.__trains_counter += 1
            else:
                Exception(f"Station {self.__stations[0].number}\n Platform 0 \nAlready has a train")
            if self.__stations[-1].get_platforms()[1].train is None:
                self.__stations[-1].get_platforms()[1].train = self.__depots[1].pull_out_train()
                self.__trains_counter += 1
            else:
                Exception(f"Station {self.__stations[1].number}\n Platform 1 \nAlready has a train")
        except Exception as text:
            print(text)

    def next_phase(self):
        self.set_time_delay()
        for i in range(len(self.__stations) - 1):
            if self.__stations[len(self.__stations) - 1].get_platforms()[0].train is not None:
                self.__depots[1].pull_into(self.__stations[len(self.__stations)-1].get_platforms()[0].train)
                self.__stations[len(self.__stations)-1].get_platforms()[0].train = None
                self.__trains_counter -= 1

            if self.__stations[i+1].get_platforms()[0].train is None:
                self.__stations[i].get_platforms()[0].train.switch_station(self.__stations[i+1].get_platforms()[0])
            elif self.__stations[i+1].get_platforms()[0].train is not None:
                continue
        for i in range(1, len(self.__stations)):
            if self.__stations[0].get_platforms()[1].train is not None:
                self.__depots[0].pull_into(self.__stations[0].get_platforms()[1].train)
                self.__stations[0].get_platforms()[1].train = None
                self.__trains_counter -= 1

            if self.__stations[i-1].get_platforms()[1].train is None:
                self.__stations[i].get_platforms()[1].train.switch_station(self.__stations[i-1].get_platforms()[1])
            elif self.__stations[i-1].get_platforms()[1].train is not None:
                continue

        self.__start_time += self.__delta_time

