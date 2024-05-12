from xml.dom.minidom import *
import xml.sax
import uuid
import os

from controller.data_controller import DataController
from controller.search_criteria import SearchCriteria

from controller.sax_handlers.get_all_products_handler import GetAllProductsHandler
from controller.sax_handlers.get_products_by_criteria import GetProductsByCriteriaHandler

from model.Product import Product


class FileController(DataController):
    def __init__(self, filepath: str):
        self.__filepath: str = filepath
        if not os.path.exists(filepath):
            self.__creation()

    def __creation(self):
        doc: Document = getDOMImplementation().createDocument(None, 'products', None)
        self.__save(doc)

    def __save(self, doc: Document) -> None:
        with open(self.__filepath, 'w') as file:
            file.write(doc.toxml())

    def get_products(self) -> list[Product]:
        handler = GetAllProductsHandler()
        xml.sax.parse(self.__filepath, handler)
        dict_products: list[dict] = handler.products
        if len(dict_products) > 0:
            dict_products.pop()
        products: list[Product] = []
        for dict_product in dict_products:
            products.append(Product(uuid.UUID(dict_product['id']), dict_product['name'],
                                    dict_product['manufacturer_name'], int(dict_product['manufacturer_id']),
                                    int(dict_product['amount_in_storage']), dict_product['storage_address']))
        return products

    def add_product(self, product: Product) -> None:
        doc: Document = parse(self.__filepath)

        xml_product = doc.createElement('product')
        xml_product.attributes['id'] = product.id.__str__()
        xml_product.attributes['name'] = product.name
        xml_product.attributes['manufacturer_name'] = product.manufacturer_name
        xml_product.attributes['manufacturer_id'] = str(product.manufacturer_id)
        xml_product.attributes['amount_in_storage'] = str(product.amount_in_storage)
        xml_product.attributes['storage_address'] = product.storage_address

        xml_products = doc.getElementsByTagName('products')[0]
        xml_products.appendChild(xml_product)

        self.__save(doc)

    def search_products(self, search_criteria: SearchCriteria) -> list[Product]:
        handler = GetProductsByCriteriaHandler(search_criteria)
        xml.sax.parse(self.__filepath, handler)
        dict_products: list[dict] = handler.products
        if len(dict_products) > 0:
            dict_products.pop()
        products: list[Product] = []
        for dict_product in dict_products:
            products.append(Product(uuid.UUID(dict_product['id']), dict_product['name'],
                                    dict_product['manufacturer_name'], int(dict_product['manufacturer_id']),
                                    int(dict_product['amount_in_storage']), dict_product['storage_address']))
        return products

    def delete_products(self, search_criteria: SearchCriteria) -> int:
        doc: Document = parse(self.__filepath)
        deleted_count: int = 0
        products = doc.getElementsByTagName('product')
        for i in products:
            match search_criteria.criteria:
                case 'name':
                    if (search_criteria.name == i.getAttribute('name')
                            or str(search_criteria.amount_in_storage) == i.getAttribute('amount_in_storage')):
                        self.__delete_product(i.getAttribute('id'))
                        deleted_count += 1
                case 'manufacturer':
                    if (search_criteria.manufacturer_name == i.getAttribute('manufacturer_name')
                            or str(search_criteria.manufacturer_id) == i.getAttribute('manufacturer_id')):
                        self.__delete_product(i.getAttribute('id'))
                        deleted_count += 1
                case 'address':
                    if search_criteria.storage_address == i.getAttribute('storage_address'):
                        self.__delete_product(i.getAttribute('id'))
                    deleted_count += 1
        return deleted_count

    def products_amount(self) -> int:
        handler = GetAllProductsHandler()
        xml.sax.parse(self.__filepath, handler)
        return len(handler.products) - 1

    def __delete_product(self, id: str) -> None:
        doc: Document = parse(self.__filepath)
        products = doc.getElementsByTagName('product')
        for i in products:
            if i.getAttribute('id') == id:
                parent = i.parentNode
                parent.removeChild(i)
                break
        self.__save(doc)
