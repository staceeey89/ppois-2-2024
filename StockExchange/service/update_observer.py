import threading
import time

from service.update_data_service import *


def observer(repository: AssetRepository, exchanges: list[StockExchange], traders: list[Trader],
             stop_event: threading.Event) -> None:
    while not stop_event.is_set():
        time.sleep(3)
        update_repository(repository)
        update_traders_data(traders, repository)
        update_exchanges_data(exchanges, repository)
