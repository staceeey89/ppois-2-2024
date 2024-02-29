from .credit_card import CreditCard
from datetime import datetime


class Transaction:
    def __init__(self, sender_card: CreditCard, receiver_card: CreditCard, amount: int, timestamp: datetime):
        self.sender: CreditCard = sender_card
        self.receiver: CreditCard = receiver_card
        self.amount: int = amount
        self.timestamp: datetime = timestamp
