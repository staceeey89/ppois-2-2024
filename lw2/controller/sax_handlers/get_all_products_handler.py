import xml.sax


class GetAllProductsHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.products: list[dict] = []
        self.__current_product: dict = {}

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
        self.products.append(self.__current_product)
