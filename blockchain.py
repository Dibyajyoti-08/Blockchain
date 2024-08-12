import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

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

    def register_node(self, address):
        """
        Add a new node to the blockchain.
        :param address: <str> Address of node.
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determines if the chain is valid.
        :param chain: <list> list of blocks
        :return:
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n--------------\n")
            # Check if the hash of the block is correct
            if block['previous_hash' != self.hash(last_block)]:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our Consenus Algorithm, it resolve conflicts
        by replacing out chain with the longest one in the network.
        :return: <bool> True if conflicts, False if not
        """
        neighbours = self.nodes
        new_chain = None

        # We're only looking the chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than
        if new_chain:
            self.chain = new_chain
            return True

        return False



