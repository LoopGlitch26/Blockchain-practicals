from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet.txt', 'w') as file:
                    file.write(self.public_key)
                    file.write('\n')
                    file.write(self.private_key)
            except(IOError, IndexError):
                print("Saving wallet failed!!!!")

    def load_keys(self):
        try:
            with open('wallet.txt', 'r') as file:
                keys = file.readlines()
                # Since '\n' will be a part of first line.
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
        except(IOError, IndexError):
            print("Loading wallet failed!!!")

    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def sign_transaction(self, sender, recipient, amount):
        # Converting back to 'binary' from string (we converted above).
        signer = PKCS1_v1_5.new(RSA.importKey(
            binascii.unhexlify(self.private_key)))
        # Converting to string and enconding.
        new_hash = SHA256.new(
            (str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(new_hash)
        # Converting back to 'string'
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        """Verify the signature of the transaction.
        
        Arguments:
            transaction: The transaction that should be verified.
        """
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        new_hash = SHA256.new(
            (str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(new_hash, binascii.unhexlify(transaction.signature))
