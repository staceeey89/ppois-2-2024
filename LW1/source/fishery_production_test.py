import threading
import time
import unittest
from datetime import datetime, timedelta
from typing import List
from unittest.mock import patch

from source import fisherman
from source.cold_storage import ColdStorage
from source.fish import Fish, FishState
from source.fisherman import Fisherman, Experience
from source.fishery_production import FisheryProduction
from source.market import Market
from source.net import Net
from source.ship import Ship
from util.serialization_util import Util


class FisheryProductionTest(unittest.TestCase):
    def setUp(self):
        self.cold_storage = ColdStorage("Хранилище", [], [], [])
        self.market = Market("Рынок", [])
        self.fishery_production = FisheryProduction(self.cold_storage, self.market)
        self.fisherman = Fisherman("Ваня", Experience.BEGINNER)

    def test_add_fisherman(self):
        self.fishery_production.add_fisherman()


class FishermanTest(unittest.TestCase):
    def setUp(self):
        self.fisherman = Fisherman("Ваня", Experience.BEGINNER)

    def test_catch_fish(self):
        expected_min_fish_count = 1
        expected_max_fish_count = self.fisherman.experience.value
        fishes = self.fisherman.catch_fish()
        self.assertNotEqual(len(fishes), 0)
        self.assertGreaterEqual(len(fishes), expected_min_fish_count)
        self.assertLessEqual(len(fishes), expected_max_fish_count)

    def test_to_dict(self):
        fisherman_dict = self.fisherman.to_dict()
        self.assertIsInstance(fisherman_dict, dict)
        self.assertIn('name', fisherman_dict)
        self.assertIn('experience', fisherman_dict)
        self.assertEqual(fisherman_dict['name'], "Ваня")
        self.assertEqual(fisherman_dict['experience'], Experience.BEGINNER.name)


class NetTest(unittest.TestCase):
    def setUp(self):
        self.net = Net(2)

    def test_cast(self):
        self.net.cast()
        self.assertIsNotNone(self.net.cast_time)

    def test_retrieve(self):
        is_retrieved = self.net.retrieve()
        self.assertEqual(False, is_retrieved)

    def test_retrieve_after_enough_time(self):
        self.net.cast()
        time.sleep(4)
        is_retrieved = self.net.retrieve()
        fish = self.net.store()
        self.assertEqual(True, is_retrieved)
        self.assertGreater(len(fish), 0)

    def test_set_time(self):
        self.net.set_time(datetime.now())
        self.assertEqual(self.net.cast_time + timedelta(seconds=self.net.square * 2), self.net.caught_time)

    def test_to_dict(self):
        cast_time = datetime(2024, 2, 20, 15, 30, 0)  # Пример времени
        self.net.set_time(cast_time)
        expected_dict = {
            'square': self.net.square,
            'cast_time': cast_time.isoformat()
        }
        result_dict = self.net.to_dict()
        self.assertEqual(expected_dict, result_dict)


class ColdStorageTest(unittest.TestCase):
    def setUp(self):
        self.storage = ColdStorage("Хранилище", [], [], [])
        fish1 = Fish(weight=6, species="trout", state=FishState.CAUGHT)
        fish2 = Fish(weight=7, species="salmon", state=FishState.CAUGHT)
        fish3 = Fish(weight=6, species="pike", state=FishState.CAUGHT)
        self.fish = [fish1, fish2, fish3]

    def test_cast(self):
        self.storage.store_fish(self.fish)
        self.assertIsNotNone(self.storage.fish_from_fishing)
        self.assertEqual(self.storage.fish_from_fishing[0].state.name, FishState.TRANSPORTED.name)

    def test_process_fish(self):
        self.storage.store_fish(self.fish)
        self.storage.process_fish()
        self.assertIsNotNone(self.storage.fish_after_processing)
        self.assertEqual(self.storage.fish_after_processing[0].state.name, FishState.PROCESSED.name)

    def test_freeze_fish(self):
        self.storage.store_fish(self.fish)
        self.storage.process_fish()
        self.storage.freeze_fish(20)
        total_weight = sum(fish.weight for fish in self.storage.frozen_fish)
        self.assertIsNotNone(self.storage.frozen_fish)
        self.assertEqual(self.storage.frozen_fish[0].state.name, FishState.FROZEN.name)
        self.assertLessEqual(total_weight, 20)

    def test_sell_fish_to_market(self):
        self.storage.store_fish(self.fish)
        self.storage.process_fish()
        fish_to_market = self.storage.sell_fish_to_market(20)
        self.assertLessEqual(len(fish_to_market), 20)
        self.assertEqual(fish_to_market[0].state.name, FishState.FOR_SALE.name)


class MarketTest(unittest.TestCase):
    def setUp(self):
        self.market = Market("Рынок", [])
        self.fisherman = Fisherman("Логан", Experience.EXPERT)
        fish = self.fisherman.catch_fish()
        self.cold_storage = ColdStorage("Хранилище", fish, [], [])
        self.cold_storage.process_fish()
        self.fish_for_sale = self.cold_storage.sell_fish_to_market(20)

    def test_process_market(self):
        self.market.receive_fish_from_storage(self.cold_storage, self.fish_for_sale)
        self.assertGreater(len(self.market.fish_on_market), 0)
        self.assertEqual(self.market.fish_on_market[0].state.name, FishState.FOR_SALE.name)

    def test_sell_fish(self):
        self.market.receive_fish_from_storage(self.cold_storage, self.fish_for_sale)
        total_weight_before_selling = sum(fish.weight for fish in self.market.fish_on_market)
        self.assertGreater(total_weight_before_selling, 10)
        sell_thread = threading.Thread(target=self.market.sell_fish)
        sell_thread.start()
        time.sleep(11)
        self.market.market_event.set()
        total_weight_after_selling = sum(fish.weight for fish in self.market.fish_on_market)
        self.assertLessEqual(total_weight_after_selling, 10)


class ShipTest(unittest.TestCase):
    def setUp(self):
        self.fisherman1 = Fisherman("Дмитрий", Experience.EXPERT)
        self.fisherman2 = Fisherman("Николай", Experience.EXPERT)
        self.net1 = Net(4)
        self.net2 = Net(5)
        self.ship = Ship("Победа")
        self.ship.taken_nets = [self.net1, self.net2]
        self.ship.fishermen = [self.fisherman1, self.fisherman2]
        self.cold_storage = ColdStorage("Хранилище", [], [], [])

    def test_add_net(self):
        net = Net(7)
        self.ship.add_net(net, is_casted=False)
        self.assertEqual(len(self.ship.taken_nets), 3)
        self.assertEqual(len(self.ship.casted_nets), 0)

    def test_add_fisherman(self):
        fisherman = Fisherman("Петр", Experience.ADVANCED)
        self.ship.add_fishermen([fisherman])
        self.assertEqual(len(self.ship.fishermen), 1)

    def test_transport_fish(self):
        fish = self.fisherman1.catch_fish()
        self.ship.caught_fish = fish
        caught_fish_len = len(self.ship.caught_fish)
        self.ship.transport_fish(self.cold_storage)
        self.assertEqual(caught_fish_len, len(self.cold_storage.fish_from_fishing))
        self.assertEqual(self.cold_storage.fish_from_fishing[0].state.name, FishState.TRANSPORTED.name)


class FisheryProductionTest(unittest.TestCase):
    def setUp(self):
        self.cold_storage = ColdStorage("Хранилище", [], [], [])
        self.market = Market("Рынок", [])
        self.fishery_production = FisheryProduction(self.cold_storage, self.market)
        fish1 = Fish(weight=7, species="trout", state=FishState.CAUGHT)
        fish2 = Fish(weight=7, species="salmon", state=FishState.CAUGHT)
        fish3 = Fish(weight=7, species="pike", state=FishState.CAUGHT)
        self.fish = [fish1, fish2, fish3]

    @patch('builtins.input', side_effect=["Победа"])
    def test_add_ship(self, mock_input):
        initial_ship_count = len(self.fishery_production.ships)
        self.fishery_production.add_ship()
        self.assertEqual(len(self.fishery_production.ships), initial_ship_count + 1)

    @patch('builtins.input', side_effect=[25])
    def test_add_net(self, mock_input):
        initial_net_count = len(self.fishery_production.free_nets)
        self.fishery_production.add_net()
        self.assertEqual(len(self.fishery_production.free_nets), initial_net_count + 1)

    @patch('builtins.input', side_effect=["Леша", "новичок"])
    def test_add_fisherman(self, mock_input):
        initial_fisherman_count = len(self.fishery_production.fishermen)
        self.fishery_production.add_fisherman()
        self.assertEqual(len(self.fishery_production.fishermen), initial_fisherman_count + 1)

    @patch('builtins.input', side_effect=[14])
    def test_transport_fish(self, mock_input):
        self.fishery_production.cold_storage.fish_from_fishing = self.fish
        self.fishery_production.process_fish()
        total_count_before_transport = 3
        self.fishery_production.transport_fish_to_market()
        total_count_after_transport = len(self.fishery_production.cold_storage.fish_after_processing)
        self.assertGreater(total_count_before_transport, total_count_after_transport)

    @patch('builtins.input', side_effect=["1", "1"])  # Mocking input for ship selection
    def test_organize_fishing_with_ship_and_fishermen(self, mock_input):
        fisherman = Fisherman("Вова", Experience.EXPERT)
        ship = Ship("Судно")
        self.fishery_production.ships = [ship]
        self.fishery_production.fishermen = [fisherman]
        self.fishery_production.organize_fishing()

        time.sleep(6)
        self.fishery_production.end_fishing_and_store_fish()
        self.assertGreater(len(self.fishery_production.cold_storage.fish_from_fishing), 0)


class UtilTest(unittest.TestCase):

    def test_fish_from_dict_list(self):
        fish_dict_list = [
            {'species': 'trout', 'weight': 5, 'state': 'CAUGHT'},
            {'species': 'salmon', 'weight': 7, 'state': 'CAUGHT'}
        ]
        fish_list = Util.fish_from_dict_list(fish_dict_list)
        self.assertIsInstance(fish_list, list)
        self.assertEqual(len(fish_list), 2)
        self.assertIsInstance(fish_list[0], Fish)
        self.assertEqual(fish_list[0].species, 'trout')
        self.assertEqual(fish_list[0].weight, 5)
        self.assertEqual(fish_list[0].state, FishState.CAUGHT)

    def test_create_cold_storage(self):
        cold_storage_data = {
            'name': 'Хранилище',
            'fish_from_fishing': [],
            'fish_after_processing': [],
            'frozen_fish': []
        }
        cold_storage = Util.create_cold_storage(cold_storage_data)
        self.assertIsInstance(cold_storage, ColdStorage)
        self.assertEqual(cold_storage.name, 'Хранилище')

    def test_create_market(self):
        market_data = {
            'name': 'Рынок',
            'fish_on_market': []
        }
        market = Util.create_market(market_data)
        self.assertIsInstance(market, Market)
        self.assertEqual(market.name, 'Рынок')

    def test_create_fishermen(self):
        fishermen_data = [
            {'name': 'Вася', 'experience': 'EXPERT'},
            {'name': 'Петя', 'experience': 'BEGINNER'}
        ]
        fishermen = Util.create_fishermen(fishermen_data)
        self.assertIsInstance(fishermen, list)
        self.assertEqual(len(fishermen), 2)
        self.assertIsInstance(fishermen[0], Fisherman)
        self.assertEqual(fishermen[0].name, 'Вася')
        self.assertEqual(fishermen[0].experience, Experience.EXPERT)

    def test_create_net(self):
        net_data = {'square': 10, 'cast_time': '2024-02-18T12:00:00'}
        net = Util.create_net(net_data)
        self.assertIsInstance(net, Net)
        self.assertEqual(net.square, 10)
        self.assertEqual(net.cast_time, datetime(2024, 2, 18, 12, 0, 0))

    def test_create_ships(self):
        ships_data = [{'name': 'Судно1'}, {'name': 'Судно2'}]
        ships = Util.create_ships(ships_data)
        self.assertIsInstance(ships, list)
        self.assertEqual(len(ships), 2)
        self.assertIsInstance(ships[0], Ship)
        self.assertEqual(ships[0].name, 'Судно1')


if __name__ == '__main__':
    unittest.main()
