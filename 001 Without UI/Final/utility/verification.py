"""
Privides verification helper function.
"""

from utility.hash_utils import hash_block, hash_string_256
from wallet import Wallet


class Verification:

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """Validate a proof.

        Arguments:
            transactions: Transaction of the block.
            last_hash: The stored previous_hash.
            proof: The proof we are testing.
        """
        guess = (str(
            [
                tx.to_ordered_dict()
                 for tx in transactions
                 ]
        ) +
            str(last_hash) +
            str(proof)).encode()
        # Hash the string.
        guess_hash = hash_string_256(guess)
        # Printing all the hashes performed.
        # print(guess_hash)
        # Define the conditions for a new valid hash.
        return guess_hash[0:2] == "00"

    @classmethod
    def verify_chain(cls, blockchain):
        """Verifies whether the block are matching or not."""
        for index, block in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(
                    block.transactions[:-1],
                    block.previous_hash,
                    block.proof):
                print("Proof of work is Invalid!!!")
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        """Verifies whether transaction is possible or not.

        Arguments:
            transaction: The transaction that should be verified.
            get_balance:
        """
        if check_funds:
            sender_balance = get_balance()
            print(sender_balance)
            return (sender_balance >= transaction.amount and
                    Wallet.verify_transaction(transaction))
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transaction, get_balance):
        """Verifies all the transactions."""
        return all(
            [
                cls.verify_transaction(tx, get_balance, False)
                for tx in open_transaction
            ]
        )
