import random
import sqlite3
import uuid

from controller.search_criteria import SearchCriteria
from controller.data_controller import DataController
from model.Product import Product


class DataBaseController(DataController):
    def __init__(self, file_name: str):
        if file_name == '':
            raise ValueError
        self.__connection = sqlite3.connect(file_name)
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                manufacturer_name TEXT NOT NULL,
                UNP INTEGER,
                amount_in_storage INTEGER,
                storage_address TEXT NOT NULL
            )
        ''')

    def __del__(self):
        self.__connection.commit()
        self.__connection.close()

    def get_products(self) -> list[Product]:
        self.__cursor.execute('SELECT * FROM Products')
        tuple_list: list[tuple] = self.__cursor.fetchall()
        products_list: list[Product] = []
        for i in tuple_list:
            products_list.append(Product(*i))
        return products_list

    def add_product(self, product: Product) -> None:
        self.__cursor.execute(f'INSERT INTO Products '
                              '(id, name, manufacturer_name, UNP, amount_in_storage, storage_address) '
                              'VALUES (?, ?, ?, ?, ?, ?)',
                              (product.id.__str__(), product.name, product.manufacturer_name, product.manufacturer_id,
                               product.amount_in_storage, product.storage_address))

    def search_products(self, search_criteria: SearchCriteria) -> list[Product]:
        match search_criteria.criteria:
            case 'name':
                self.__cursor.execute('SELECT * FROM Products WHERE name = ? OR amount_in_storage = ?',
                                      (search_criteria.name, search_criteria.amount_in_storage))
            case 'manufacturer':
                self.__cursor.execute('SELECT * FROM Products WHERE manufacturer_name = ? OR UNP = ?',
                                      (search_criteria.manufacturer_name, search_criteria.manufacturer_id))
            case 'address':
                self.__cursor.execute('SELECT * FROM Products WHERE storage_address = ?',
                                      (search_criteria.storage_address,))
        search_list: list[tuple] = self.__cursor.fetchall()
        search_product_list: list[Product] = []
        for i in search_list:
            search_product_list.append(Product(*i))
        return search_product_list

    def delete_products(self, search_criteria: SearchCriteria) -> int:
        amount_of_deleted_products = len(self.search_products(search_criteria))
        match search_criteria.criteria:
            case 'name':
                self.__cursor.execute('DELETE FROM Products WHERE name = ? OR amount_in_storage = ?',
                                      (search_criteria.name, search_criteria.amount_in_storage))
            case 'manufacturer':
                self.__cursor.execute('DELETE FROM Products WHERE manufacturer_name = ? OR UNP = ?',
                                      (search_criteria.manufacturer_name, search_criteria.manufacturer_id))
            case 'address':
                self.__cursor.execute('DELETE FROM Products WHERE storage_address = ?',
                                      (search_criteria.storage_address,))
        return amount_of_deleted_products

    def products_amount(self) -> int:
        self.__cursor.execute('SELECT COUNT(*) FROM Products')
        return int(self.__cursor.fetchone()[0])
