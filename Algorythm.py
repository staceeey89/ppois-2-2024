from KeyClass import Key


class Algorythm:
    __doc__ = "class represents an algorythm for encryption device"
    __name: str = ""
    __key: Key = None

    def __init__(self, name_: str, key_: Key):
        self.__key = key_
        self.__name = name_

    def manage_key(self):
        self.__key.manage_keys()

    def caesar_encryption(self, data_: str, flag: bool) -> str:
        encrypted_data: str = ""
        for char in data_:
            if char.isalpha():
                ascii_offset: int = 65 if char.isupper() else 97
                if flag == 1:
                    encrypted_char: str = chr((ord(char)
                                               - ascii_offset - self.__key.key)
                                              % 26 + ascii_offset
                                              )
                else:
                    encrypted_char: str = chr((ord(char)
                                               - ascii_offset + self.__key.key)
                                              % 26 + ascii_offset
                                              )

                encrypted_data += encrypted_char
            else:
                encrypted_data += char
        return encrypted_data


    def caesar_analyze(self, encrypted_data_: str, expected_data: str) -> int:
        for shift in range(0, 100):
            deencrypt_data: str = ""
            for char in encrypted_data_:
                if char.isalpha():
                    ascii_offset: int = 65 if char.isupper() else 97
                    encrypted_char: str = chr((ord(char)
                                               - ascii_offset + shift)
                                              % 26 + ascii_offset
                                              )
                    deencrypt_data += encrypted_char
                else:
                    deencrypt_data += char
            if expected_data == deencrypt_data:
                return shift
