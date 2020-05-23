from functools import reduce
import hashlib
from collections import OrderedDict
import pickle

from hash_utils import hash_block, hash_string_256

# The reward given to the miners (for creating a new block).
MINING_REWARD = 10

# The starting block of blockchain.
genesis_block = {"previous_hash": "",
                 "index": 0,
                 "transaction": [],
                 "proof": 100
                 }
# Initailizing our (empty) blockchain list.
blockchain = [genesis_block]
# Unhandeled transaction.
open_transaction = list()
# The owner of this blockchain node
owner = "Mayank"
# Registered participants.
participants = {"Mayank"}


def load_data():
    with open("blockchain.data", 'rb') as file:
        file_content = pickle.loads(file.read())
        global blockchain
        global open_transaction
        blockchain = file_content["chain"]
        open_transaction = file_content["open_tx"]


load_data()


def save_data():
    with open("blockchain.data", 'wb') as file:     # We can use any extension.
        save_data = {
            'chain': blockchain,
            'open_tx': open_transaction
        }
        file.write(pickle.dumps(save_data))


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    # Hash the string.
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    # Define the conditions for a new valid hash.
    return guess_hash[0:2] == "00"


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transaction, last_hash, proof):
        proof += 1
        # Printing the number of hashes done to check the proof.
        print(proof)
    return proof


def get_balance(participant):
    """Name of the participant as the parameter."""
    tx_sender = [[tx['amount'] for tx in block["transaction"]
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transaction if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                         if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block["transaction"]
                     if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                             if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # Returns total balance.
    return amount_recieved - amount_sent


def get_last_blockchain_value():
    """Returns the last value of the current blockchain."""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    """Verifies whether transaction is possible or not."""
    sender_balance = get_balance(transaction['sender'])
    print(sender_balance)
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
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
    transaction = OrderedDict(
        [("sender", sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transaction.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    # print(hashed_block)
    proof = proof_of_work()
    # Miners should be rewarded for there work.
    reward_transaction = OrderedDict(
        [('sender', "MINING"), ('recipient', owner), ('amount', MINING_REWARD)])
    # reward_transaction = {
    #    'sender': "MINING",
    #    'recipient': owner,
    #    'amount': MINING_REWARD
    # }
    # Copy transaction instead of manipulating the orignal "open_transactions".
    copied_transaction = open_transaction[:]
    copied_transaction.append(reward_transaction)
    block = {"previous_hash": hashed_block,
             "index": len(blockchain),
             "transaction": copied_transaction,
             "proof": proof
             }
    blockchain.append(block)
    return True


def get_transaction_value():
    """Returns the input of the user (a new transaction amount) as a float."""
    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Your Transaction amount ----> "))
    return tx_recipient, tx_amount


def get_user_choice():
    """Taking the integer input from the user regarding the choice."""
    user_input = input("Enter your choice: ")
    return user_input


def print_blockchian_elements():
    """Prints all the blocks in the list."""
    for block in blockchain:
        print("Printing all the blocks!")
        print(block)
    else:
        print("-" * 20)


def verify_chain():
    """Verifies whether the block are matching or not."""
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block["transaction"][:-1], block["previous_hash"], block['proof']):
            print("Proof of work is Invalid!!!")
            return False
    return True


def verify_transactions():
    """Verifies all the transactions."""
    return all([verify_transaction(tx) for tx in open_transaction])


"""A condition for our while loop (default True)
To come out of loop, it will be changed to False."""
waiting_for_input = True

if __name__ == "__main__":
    while waiting_for_input:
        print("Please Select:")
        print("1. Enter the transaction amount.")
        print("2. Mine a new block.")
        print("3. Output the blockchain block")
        print("4. Output participants")
        print("5. Check transaction validity")
        print("h. Manipulate the Block")
        print("q. Quit")
        user_choice = get_user_choice()
        print()

        if user_choice == '1':
            tx_data = get_transaction_value()
            recipient, amount = tx_data
            # Add the transaction amount to the blockchain.
            if add_transaction(recipient, amount=amount):
                print("Added Transaction!!")
            else:
                print("Transaction Failed!")
            print(open_transaction)

        elif user_choice == '2':
            if mine_block():
                # Resets the open_transaction to an empty list.
                open_transaction = []
                save_data()

        elif user_choice == '3':
            print_blockchian_elements()

        elif user_choice == '4':
            print(participants)

        elif user_choice == '5':
            if verify_transactions():
                print('All transactions are valid!')
            else:
                print('There are invalid transactions!')

        elif user_choice == 'h':
            # Make sure that the blockchain is not "hackacble" if it is empty.
            if len(blockchain) >= 1:
                blockchain[0] = {"previous_hash": "",
                                 "index": 0,
                                 "transaction": [{"sender": "Alpha", "recipient": "Beta", "amount": 100.0}]
                                 }
        elif user_choice == 'q':
            waiting_for_input = False
        else:
            print("Invalid Input!!")
            print("Exiting after printing the blocks")
            print_blockchian_elements()
            break

        if not verify_chain():
            print_blockchian_elements()
            print("Invalid Blockchain!")
            break

        print('Balance of {}: {:6.4f}'.format(
            "Mayank", get_balance("Mayank")))
    else:
        print("User Logged Out!")
