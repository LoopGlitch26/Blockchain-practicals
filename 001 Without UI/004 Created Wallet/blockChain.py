from functools import reduce
import hashlib
import json

from utility.hash_utils import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

# The reward given to the miners (for creating a new block).
MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_ID):
        # The starting block of blockchain.
        genesis_block = Block(0, "", [], 100, 0)
        # Initailizing our (empty) blockchain list.     Making it private.
        self.__chain = [genesis_block]
        # Unhandeled transaction.                       Making it private.
        self.__open_transaction = list()
        self.load_data()
        self.hosting_node = hosting_node_ID

    def get_chain(self):
        return self.__chain[:]

    def get_open_transaction(self):
        return self.__open_transaction[:]

    def load_data(self):
        """Initialize by loading data from a file"""
        try:

            with open("blockchain.txt", 'r') as file:
                file_content = file.readlines()

                # To remove the "\n" from the load, we are using range selector.
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = list()

                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                open_transaction = json.loads(file_content[1])
                updated_transactions = list()
                for tx in open_transaction:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transaction = updated_transactions

        except (IOError, IndexError):
            print("Exception HANDLED")
            pass

    def save_data(self):
        try:
            # We can use any extension.
            with open("blockchain.txt", 'w') as file:
                new_saveable_chain = [block.__dict__ for block in [Block(new_block.index, new_block.previous_hash, [
                    tx.__dict__ for tx in new_block.transactions], new_block.proof, new_block.timestamp) for new_block in self.__chain]]
                file.write(json.dumps(new_saveable_chain))
                file.write('\n')
                new_saveable_tx = [
                    block.__dict__ for block in self.__open_transaction]
                file.write(json.dumps(new_saveable_tx))
        except IOError:
            print("Saving Failed!!")

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transaction, last_hash, proof):
            proof += 1
            # Printing the number of hashes done to check the proof.
            # print(proof)
        return proof

    def get_balance(self):
        """Name of the participant as the parameter.
        """
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount
                          for tx in self.__open_transaction if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                             if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]
        amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                                 if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        # Returns total balance.
        return amount_recieved - amount_sent

    def get_last_blockchain_value(self):
        """Returns the last value of the current blockchain."""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """Append new value as well as last value to blockchain.

        Arguments:
            :sender: The sender of the coin.
            :recipient: The recipient of the coin.
            :amount: The amount of coin sent with the transaction (default = 1.0).
        """
        # transaction = {
        #    'sender': sender,
        #    'recipient': recipient,
        #    'amount': amount
        # }
        if self.hosting_node == None:
            return False

        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transaction.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        if self.hosting_node == None:
            return False

        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        # print(hashed_block)
        proof = self.proof_of_work()
        # Miners should be rewarded for there work.
        reward_transaction = Transaction(
            "MINING", self.hosting_node, '', MINING_REWARD)
        # reward_transaction = {
        #    'sender': "MINING",
        #    'recipient': owner,
        #    'amount': MINING_REWARD
        # }
        # Copy transaction instead of manipulating the orignal "open_transactions".
        copied_transaction = self.__open_transaction[:]
        for tx in copied_transaction:
            if not Wallet.verify_transaction(tx):
                return False
        copied_transaction.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transaction, proof)

        self.__chain.append(block)
        # Resets the open_transaction to an empty list.
        self.__open_transaction = []
        self.save_data()
        return True
