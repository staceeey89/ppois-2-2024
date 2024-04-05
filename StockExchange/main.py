import msvcrt
import random
import sys
from datetime import date

from model.asset import Asset
from model.bond import Bond
from model.share import Share
from model.broker import Broker
import threading
from util.menu import *
import time
from serialization.serialization import *

from service.update_data_service import *
from service.update_observer import observer

if __name__ == '__main__':
    repository = deserialize_object('database/repository.txt')
    brokers = deserialize_object('database/brokers.txt')
    exchanges = deserialize_object('database/exchanges.txt')
    traders = deserialize_object('database/traders.txt')
    for broker in brokers:
        new_ex = set()
        for trader_exchange in broker.exchanges:
            for exchange in exchanges:
                if trader_exchange.name == exchange.name:
                    new_ex.add(exchange)
        broker.exchanges = new_ex

    for trader in traders:
        for broker in brokers:
            if trader.broker.name == broker.name:
                trader.broker = broker

    stop_event = threading.Event()
    t = threading.Thread(target=observer, args=(repository, exchanges, traders, stop_event))
    t.start()

    choice = ''
    while True:
        print_main_menu()
        choice = input()
        if choice == 'exit':
            break
        current_trader = None
        for broker in traders:
            if broker.name == choice:
                current_trader = broker
                break
        if not isinstance(current_trader, Trader):
            print('No such trader')
            continue
        while True:
            print_trader_menu(current_trader)
            try:
                choice = int(input())
                if choice == 1:
                    print_trader_portfolio(current_trader)
                    input('press any symbol')
                elif choice == 2:
                    try:
                        change_broker(current_trader, brokers, input('Write name of your broker'))
                        input('press any symbol')
                    except InputException as e:
                        print(f'{e}')
                elif choice == 3:
                    print(current_trader.broker.info())
                    input('press any symbol')
                elif choice == 4:
                    try:
                        symbol = input('Write symbol of asset')
                        amount = int(input('Write amount of assets'))
                        if amount < 1:
                            raise ValueError('Amount must be more than 0')
                        buy(current_trader, current_trader.broker.get_all_assets(), symbol, amount)
                    except ValueError as e:
                        print(f'{e}')
                    except BuySellException as e:
                        print(f'{e}')
                elif choice == 5:
                    try:
                        symbol = input('Write symbol of asset')
                        amount = int(input('Write amount of assets'))
                        if amount < 1:
                            raise ValueError('Amount must be more than 0')
                        sell(current_trader, symbol, amount)
                    except ValueError as e:
                        print(f'{e}')
                    except BuySellException as e:
                        print(f'{e}')
                elif choice == 6:
                    print_brokers(brokers)
                    input('press any symbol')
                elif choice == 7:
                    break
                else:
                    raise ValueError()
            except ValueError:
                print('Incorrect input')
                continue

    stop_event.set()
    serialize_object(repository, 'database/repository.txt')
    serialize_object(exchanges, 'database/exchanges.txt')
    serialize_object(brokers, 'database/brokers.txt')
    serialize_object(traders, 'database/traders.txt')
