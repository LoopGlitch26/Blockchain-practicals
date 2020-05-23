import json
import hashlib


def hash_string_256(string):
    """Create a SHA256 hash for a given input string.

    Arguments:
        :string: The string which should be hashed.
    """
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """Hashing a block and returns a string reprensentation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [
        tx.to_ordered_dict()
        for tx in hashable_block['transactions']
    ]
    # Converting the "block" (which is dictionary) to 'string' and then
    #  encoding it to UTF-8.
    return hash_string_256(
        json.dumps(hashable_block, sort_keys=True).encode()
    )
