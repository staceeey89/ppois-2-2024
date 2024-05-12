import xml.sax

from controller.search_criteria import SearchCriteria


class GetProductsByCriteriaHandler(xml.sax.ContentHandler):
    def __init__(self, search_criteria: SearchCriteria):
        self.products: list[dict] = []
        self.__current_product: dict = {}
        self.__search_criteria: SearchCriteria = search_criteria

    def startElement(self, name, attrs):
        self.__current_product = {
            'id': attrs.get('id'),
            'name': attrs.get('name'),
            'manufacturer_name': attrs.get('manufacturer_name'),
            'manufacturer_id': attrs.get('manufacturer_id'),
            'amount_in_storage': attrs.get('amount_in_storage'),
            'storage_address': attrs.get('storage_address')
        }

    def characters(self, content):
        pass

    def endElement(self, name):
        match self.__search_criteria.criteria:
            case 'name':
                if (self.__search_criteria.name != self.__current_product['name']
                        and str(self.__search_criteria.amount_in_storage) != self.__current_product['amount_in_storage']):
                    return
            case 'manufacturer':
                if (self.__search_criteria.manufacturer_name != self.__current_product['manufacturer_name']
                        and str(self.__search_criteria.manufacturer_id) != self.__current_product['manufacturer_id']):
                    return
            case 'address':
                if self.__search_criteria.storage_address != self.__current_product['storage_address']:
                    return
        self.products.append(self.__current_product)
