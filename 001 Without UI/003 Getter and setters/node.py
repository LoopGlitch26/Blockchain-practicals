from uuid import uuid4

from blockChain import Blockchain
from verification import Verification

class Node:

    def __init__(self):
        #self.id = str(uuid4())
        self.id = "Mayank"
        self.blockchain = Blockchain(self.id)
        

    def get_transaction_value(self):
        """Returns the input of the user (a new transaction amount) as a float."""
        tx_recipient = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Your Transaction amount ----> "))
        return tx_recipient, tx_amount

    def get_user_choice(self):
        """Taking the integer input from the user regarding the choice."""
        user_input = input("Enter your choice: ")
        return user_input

    def print_blockchian_elements(self):
        """Prints all the blocks in the list."""
        for block in self.blockchain.chain:
            print("Printing all the blocks!")
            print(block)
        else:
            print("-" * 20)

    def listen_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print("Please Select:")
            print("1. Enter the transaction amount.")
            print("2. Mine a new block.")
            print("3. Output the blockchain block")
            print("4. Check transaction validity")
            print("q. Quit")
            user_choice = self.get_user_choice()
            print()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                # Add the transaction amount to the blockchain.
                if self.blockchain.add_transaction(recipient, sender = self.id, amount=amount):
                    print("Added Transaction!!")
                else:
                    print("Transaction Failed!")
                print(self.blockchain.get_open_transaction())

            elif user_choice == '2':
                self.blockchain.mine_block()

            elif user_choice == '3':
                self.print_blockchian_elements()

            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transaction(), self.blockchain.get_balance):
                    print('All transactions are valid!')
                else:
                    print('There are invalid transactions!')

            elif user_choice == 'q':
                waiting_for_input = False

            else:
                print("Invalid Input!!")
                print("Exiting after printing the blocks")
                self.print_blockchian_elements()
                break

            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchian_elements()
                print("Invalid Blockchain!")
                break

            print('Balance of {}: {:6.4f}'.format(
                self.id, self.blockchain.get_balance()))
        else:
            print("User Logged Out!")


node = Node()
node.listen_for_input()