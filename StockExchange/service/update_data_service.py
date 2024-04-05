import random

from model.share import Share
from model.currency import Currency
from model.stock_exchange import StockExchange
from model.trader import Trader
from repository.assetrepository import AssetRepository


def update_traders_data(traders: list[Trader], repository: AssetRepository):
    asset_price = dict()
    for asset in repository.assets:
        if isinstance(asset, Currency):
            asset_price[asset] = asset.exchange_rate
        elif isinstance(asset, Share):
            asset_price[asset] = asset.price

    for trader in traders:
        for asset in trader.portfolio:
            if isinstance(asset, Currency):
                asset.exchange_rate = asset_price[asset]
            elif isinstance(asset, Share):
                asset.price = asset_price[asset]


def update_exchanges_data(exchanges: list[StockExchange], repository: AssetRepository) -> None:
    asset_price = dict()
    for asset in repository.assets:
        if isinstance(asset, Currency):
            asset_price[asset] = asset.exchange_rate
        elif isinstance(asset, Share):
            asset_price[asset] = asset.price

    for exchange in exchanges:
        for asset in exchange.assets:
            if isinstance(asset, Currency):
                asset.exchange_rate = asset_price[asset]
            elif isinstance(asset, Share):
                asset.price = asset_price[asset]


def update_repository(repository: AssetRepository) -> None:
    for asset in repository.assets:
        if isinstance(asset, Currency):
            asset.exchange_rate = asset.exchange_rate * (1 + random.choice([-1, 0, 1]) * 0.03)
        elif isinstance(asset, Share):
            asset.price = asset.price * (1 + random.choice([-1, 0, 1]) * 0.03)
