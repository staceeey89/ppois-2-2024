from model.Product import Product
from controller.search_criteria import SearchCriteria


class DataController:
    def get_products(self) -> list[Product]:
        pass

    def add_product(self, product: Product) -> None:
        pass

    def delete_products(self, search_criteria: SearchCriteria) -> int:
        pass

    def search_products(self, search_criteria: SearchCriteria) -> list[Product]:
        pass

    def products_amount(self) -> int:
        pass
