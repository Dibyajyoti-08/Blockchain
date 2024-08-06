import hashlib
import json

from time import time
from uuid import uuid4

class Bliockchain(object):
    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
          - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
          - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: Does hash(last_proof, proof) contain leading 4 zeroes?
        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :return: <bool> True if correct, False otherwise
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'