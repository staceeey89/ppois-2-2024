from Class.Certificate import *

class Standard:
    certificats = []
    def __init__(self,standart_number):
        self.standart_number = standart_number

    def AddCertificate(self, certificate: Certificate):
        self.certificats.insert(0,certificate)

    def get_certificats(self):
        return self.certificats

    def set_standart(self, number_std):
        self.standart_number = number_std
    def get_standart(self):
        return self.standart_number