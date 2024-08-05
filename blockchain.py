import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Creation of the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        '''
        Create a new block in the blockchain.
        :param proof: <int> The proof given by the proof of work algorithm
        :param previous_hash: (Optional) <str> Hash of previous block
        :return: <dict> New block
        '''

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transaction
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        '''
        Creates a new transaction to go into the chain.
        :param sender: <str> Sender's public key or address of the sender
        :param recipient: <str> Recipient's public key or address of the recipient'
        :param amount: <int> Amount
        :return: <int> The index of the block that will hold this transaction
        '''

        self.current_transactions.append({
            'sender': sender,
            'recipent': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        '''
        Creates a SHA-256 hash of a block
        :param block: <dict> Block
        :return: <str>
        '''

        # To make Dictionary is ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


