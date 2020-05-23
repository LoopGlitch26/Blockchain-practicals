import json
import hashlib


def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """Hashing a block and returns a string reprensentation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    # Converting the "block" (which is dictionary) to 'string' and then encoding it to UTF-8.
    return hash_string_256(json.dumps(block, sort_keys=True).encode())