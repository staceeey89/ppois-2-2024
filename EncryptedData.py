class EncryptedData:
    __doc__ = "encrypted data"
    data: str = None

    def __init__(self, data_: str):
        self.data = data_
