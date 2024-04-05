from model.asset import Asset


class AssetRepository:
    def __init__(self, assets: set[Asset]):
        self.__assets__ = assets

    @property
    def assets(self) -> set[Asset]:
        return self.__assets__

    @assets.setter
    def assets(self, assets: set[Asset]) -> None:
        self.__assets__ = assets
