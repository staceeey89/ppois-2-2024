from Algorythm import Algorythm
from Data import Data
from EncryptedData import EncryptedData
from KeyClass import Key


def menu():
    global temp_key
    print("--------------- Encryption device ------------------")
    print("Enter a key for encrypting data using caesar encryption")
    flag = True
    while flag:
        temp_key = int(input())
        if 26 > temp_key > 0:
            flag = False
        else:
            print("Impossible key, try again -> ")
    device = EncryptionDevice(Algorythm("Caesar", Key(temp_key)))
    choice: int = None
    while choice != 8:

        # if device.security():
        if True:
            print("1 - enter a sentence for encrypting\n"
                  "2 - encrypt data\n"
                  "3 - show encrypted data\n"
                  "4 - decipher encrypted data\n"
                  "5 - show data\n"
                  "6 - analyze caesars encryption algorythm\n"
                  "7 - manage key\n"
                  "8 - exit\n")
            choice = int(input())
            if choice == 1:
                print("Enter data -> ")
                data = Data(input())
                device.set_data(data)
            elif choice == 2:
                device.encrypt_data()
            elif choice == 3:
                device.show_encrypted_data()
            elif choice == 4:
                device.decipher_data()
            elif choice == 5:
                device.show_original_data()
            elif choice == 6:
                device.analyze_algorythm()
            elif choice == 7:
                device.get_algorythm().manage_key()
            elif choice == 8:
                break
            else:
                print("wrong choice, try again -> ")
        else:
            print("Rejected")
        print("--------------------")
    print("bye bye")


class EncryptionDevice:
    __doc__ = "device uses algorythm to encrypt data"
    __data: Data = Data("")
    __algorythm: Algorythm = None
    __en_data: EncryptedData = EncryptedData("")
    __password: str = "12qw"

    def get_algorythm(self):
        return self.__algorythm

    def __init__(self, algorythm_: Algorythm):
        self.__algorythm = algorythm_

    def set_data(self, data: Data):
        self.__data = data

    def encrypt_data(self):
        if self.__data.data == "":
            print("There is no data for encrypting")
        else:
            self.__en_data.data = self.__algorythm.caesar_encryption(self.__data.data, bool(0))
            print("data encrypted")

    def show_encrypted_data(self):
        if self.__en_data.data == "":
            print("There is no encrypted data")
        else:
            print("Encrypted Data: ", self.__en_data.data)

    def decipher_data(self):
        if self.__en_data.data == "":
            print("There is no encrypted data for deciphering")
        else:
            print("Deciphered Data: ", self.__algorythm.caesar_encryption(self.__en_data.data, bool(1)))

    def show_original_data(self):
        if self.__data.data == "":
            print("There is no data")
        else:
            print("Original Data: ", self.__data.data)

    def analyze_algorythm(self):
        if self.__data.data == "" or self.__en_data.data == "":
            print("lack of data ")
        else:
            print("Code was broken in ", self.__algorythm.caesar_analyze(self.__en_data.data, self.__data.data),
                  "iterations")

    def security(self) -> bool:
        print("Enter a security code ->")
        is_approved: bool = False
        if input() == self.__password:
            is_approved = True
        return is_approved
