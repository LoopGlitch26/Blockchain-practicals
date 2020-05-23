from collections import OrderedDict
from utility.printable import Printable

class Transaction(Printable):
    """A transaction which can be added to a block in the blockchain.
    
    Arguments:
        sender: The sender of coins.
        recipient: The recipient of coins.
        signature: The signature of the transaction.
        amount: The amount of coins sent.
    """
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])