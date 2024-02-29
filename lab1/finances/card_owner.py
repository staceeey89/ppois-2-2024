from typing import Optional


class CardOwner:
    def __init__(self, name: str, address: str, email: Optional[str], phone: str):
        self.name: str = name
        self.address: str = address
        self.email: Optional[str] = email
        self.phone: str = phone
        