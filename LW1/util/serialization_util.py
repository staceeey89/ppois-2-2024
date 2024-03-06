import json
from datetime import datetime
from typing import List

from source.cold_storage import ColdStorage
from source.fish import FishState, Fish
from source.fisherman import Experience, Fisherman
from source.market import Market
from source.net import Net
from source.ship import Ship


class Util:
    @staticmethod
    def save_state(filename: str, fishery_production) -> None:
        with open(filename, 'w') as f:
            data = fishery_production.to_dict()
            json.dump(data, f)

    @staticmethod
    def load_state(filename: str) -> dict:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data

    @staticmethod
    def fish_from_dict_list(fish_dict_list: list) -> List[Fish]:
        fish_list = []
        for fish_data in fish_dict_list:
            species = fish_data['species']
            weight = fish_data['weight']
            state = FishState[fish_data['state']]
            fish_object = Fish(weight, species, state)
            fish_list.append(fish_object)
        return fish_list

    @staticmethod
    def create_cold_storage(data: dict) -> ColdStorage:
        return ColdStorage(
            data['name'],
            Util.fish_from_dict_list(data['fish_from_fishing']),
            Util.fish_from_dict_list(data['fish_after_processing']),
            Util.fish_from_dict_list(data['frozen_fish'])
        )

    @staticmethod
    def create_market(data: dict) -> Market:
        return Market(
            data['name'],
            Util.fish_from_dict_list(data['fish_on_market'])
        )

    @staticmethod
    def create_fishermen(data: list) -> List[Fisherman]:
        fishermen = []
        for fisherman_data in data:
            name = fisherman_data['name']
            experience = Experience[fisherman_data['experience']]
            fishermen.append(Fisherman(name, experience))
        return fishermen

    @staticmethod
    def create_nets(data: list) -> List[Net]:
        return [Util.create_net(net_data) for net_data in data]

    @staticmethod
    def create_net(data: dict) -> Net:
        square = data['square']
        net = Net(square)
        cast_time = data.get('cast_time')
        if cast_time:
            try:
                net.set_time(datetime.fromisoformat(cast_time))
            except AttributeError:
                pass
        return net

    @staticmethod
    def create_ships(data: list) -> List[Ship]:
        return [Util.create_ship(ship_data) for ship_data in data]

    @staticmethod
    def create_ship(data: dict) -> Ship:
        name = data['name']
        ship = Ship(name)
        ship.fishing_event.clear()
        return ship

    @staticmethod
    def create_borrowed_ships(data: list) -> List[Ship]:
        return [Ship(**ship_data) for ship_data in data]

    @staticmethod
    def create_borrowed_fishermen(data: list) -> List[Fisherman]:
        return [Fisherman(**fisherman_data) for fisherman_data in data]

    @staticmethod
    def create_borrowed_nets(data: list) -> List[Net]:
        return [Util.create_net(net_data) for net_data in data]
