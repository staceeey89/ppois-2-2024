from model.Product import Product


class SearchCriteria:
    def __init__(self, name: str | None = None, manufacturer_name: str | None = None, manufacturer_id: int | None = None,
                 amount_in_storage: int | None = None, storage_address: str | None = None, criteria: str | None = None):
        match criteria:
            case 'name':
                if name == '' or amount_in_storage is None:
                    raise AttributeError
            case 'manufacturer':
                if manufacturer_name == '' or manufacturer_id is None:
                    raise AttributeError
            case 'address':
                if storage_address == '':
                    raise AttributeError

        self.__name = name
        self.__manufacturer_name = manufacturer_name
        self.__manufacturer_id = manufacturer_id
        self.__amount_in_storage = amount_in_storage
        self.__storage_address = storage_address
        self.__criteria = criteria

    def check(self, product: Product):
        match self.__criteria:
            case 'name':
                return self.__name == product.name or self.__amount_in_storage == product.amount_in_storage
            case 'manufacturer':
                return (self.__manufacturer_name == product.manufacturer_name or
                        self.__manufacturer_id == product.manufacturer_id)
            case 'address':
                return self.__storage_address == product.storage_address

    @property
    def name(self):
        return self.__name

    @property
    def manufacturer_name(self):
        return self.__manufacturer_name

    @property
    def manufacturer_id(self):
        return self.__manufacturer_id

    @property
    def amount_in_storage(self):
        return self.__amount_in_storage

    @property
    def storage_address(self):
        return self.__storage_address

    @property
    def criteria(self):
        return self.__criteria
