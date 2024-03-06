import copy
import logging
import threading
import time
from typing import List
import copy

from fisherman import Experience
from cold_storage import ColdStorage
from fish import Fish
from fisherman import Fisherman
from net import Net


class Ship:
    def __init__(self, name: str) -> None:
        self.fishermen = []
        self.name = name
        self.caught_fish: List[Fish] = []
        self.taken_nets = []
        self.casted_nets = []
        self.fishing_event = threading.Event()

    def start_fishing(self) -> None:
        for taken_net in self.taken_nets.copy():
            taken_net.cast()
            self.taken_nets.remove(taken_net)
            self.casted_nets.append(taken_net)
        while not self.fishing_event.is_set():
            time.sleep(5)
            for fisherman in self.fishermen:
                self.caught_fish.extend(fisherman.catch_fish())
            for casted_net in self.casted_nets.copy():
                if casted_net.retrieve():
                    # casted_net.store().extend(casted_net.caught_fish)
                    self.caught_fish.extend(casted_net.store())
                    self.taken_nets.append(casted_net)
                    self.casted_nets.remove(casted_net)

    def transport_fish(self, cold_storage: ColdStorage) -> None:
        print(f"Судно {self.name} завершает рыбалку")
        cold_storage.store_fish(self.caught_fish)
        self.caught_fish = []
        self.fishermen = []
        self.casted_nets = []
        self.taken_nets = []

    def add_net(self, net: Net, is_casted: bool) -> None:
        if is_casted:
            self.casted_nets.append(net)
        else:
            self.taken_nets.append(net)

    def add_fishermen(self, fishermen: List[Fisherman]) -> None:
        self.fishermen = fishermen

    def __str__(self) -> str:
        return f"Корабль: {self.name}"

    def get_fishing_event(self) -> threading.Event:
        return self.fishing_event

    def set_fishing_event(self) -> None:
        self.fishing_event.clear()

    def to_dict(self) -> dict:
        return {
            'name': self.name
        }
