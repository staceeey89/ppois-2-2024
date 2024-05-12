import uuid


class Product:
    def __init__(self, id: uuid.UUID, name: str, manufacturer_name: str, manufacturer_id: int,
                 amount_in_storage: int, storage_address: str):
        self.__id = id
        self.__name: str = name
        self.__manufacturer_name: str = manufacturer_name
        self.__manufacturer_id: int = manufacturer_id
        self.__amount_in_storage: int = int(amount_in_storage)
        self.__storage_address: str = storage_address

    @property
    def id(self):
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def manufacturer_name(self) -> str:
        return self.__manufacturer_name

    @property
    def manufacturer_id(self) -> int:
        return self.__manufacturer_id

    @property
    def amount_in_storage(self) -> int:
        return self.__amount_in_storage

    @property
    def storage_address(self) -> str:
        return self.__storage_address

    @amount_in_storage.setter
    def amount_in_storage(self, new_amount) -> None:
        self.__amount_in_storage = new_amount

    def tuple(self):
        values_tuple: tuple = (
            self.__id.__str__(),
            self.__name,
            self.__manufacturer_name,
            self.__manufacturer_id,
            self.__amount_in_storage if self.__amount_in_storage > 0 else 'Нет на складе',
            self.__storage_address
        )
        return values_tuple

    def __eq__(self, other):
        return self.__id == other.id

    def __str__(self):
        return (f'Product with id {self.__id}: \n\tname - {self.__name}; \n\tmanufacturer name - '
                f'{self.__manufacturer_name}; \n\tmanufacturer id - {self.__manufacturer_id}; '
                f'\n\tamount in storage - {self.__amount_in_storage}; \n\tstorage address - {self.__storage_address}')
