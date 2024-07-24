import hashlib 
import json
import time
import random
import math
from Network_cyper1 import MerkleTree, hash
from Network_VM1 import Smartcontract_container, Transaction_container, ExeSmartcontract

class Blockchain(object):
    
    def __init__(self, name):
        self.chain = []                                   
        self.current_transactions = Transaction_container()
        self.current_smartcontracts = Smartcontract_container()
        self.new_block(previous_hash='genesis_block', address = '0')          
    
    @property
    def last_block(self):
        return self.chain[-1]                             
    
    @property
    def transaction(self):
        return len(self.current_transaction)                                 

    def pick_winner(self, candidate_list) :
        random.shuffle(candidate_list)
        winner = candidate_list[0]
        return winner
    
    def pick_final_winner(self, winner_list) :
        final_winner = max(winner_list,key = winner_list.count)
        return final_winner

    def new_transaction(self, transaction):
        newer_transaction = self.current_transactions.new_transaction(transaction)
        if newer_transaction['transaction_type'] == "log" :
            response = self.current_transactions.new_transaction(transaction)
            print(response)
        elif newer_transaction['transaction_type'] == "play" and "smartcontract" in newer_transaction: 
            response = ExeSmartcontract(self.current_smartcontracts, transaction)
            print(response)
        elif newer_transaction['transaction_type'] == "register"  and "smartcontract" in newer_transaction:
            for smartcontract in self.current_smartcontracts.smartcontracts_list :
                if not newer_transaction["smartcontract"]["smartcontract_type"] in smartcontract :
                    smartcontract_List = self.current_smartcontracts.new_smartcontracts_list(newer_transaction["smartcontract"]["smartcontract_type"])
                    print(smartcontract_List)
                response = self.current_smartcontracts.new_smartcontract(newer_transaction["smartcontract"])
                print(response)
        
        return response

    def new_chain(self, chain) :
        self.chain = chain
        return len(self.chain)

    def mine_block(self, previous_hash='0'):
        hash_smartcontracts = MerkleTree(self.current_smartcontracts.return_hashList())
        blockHeader = {
            'index' : len(self.chain)+1,
            'timestamp' : time.time(),
            'previous_hash' : previous_hash or self.hash(self.chain[-1]['blockHash']),
            'transactions_hash' : self.current_transactions.get_transaction_hash(),
            'smartcontract_hash' : hash_smartcontracts.get_root(),
        }
        raw_block = {
            'blockHeader' : blockHeader,
            'blockData' : self.current_transactions.get_transaction_container(),
        }
        block = {
            'block' : raw_block,
        }
        block["blockHash"] = hash(raw_block)
        return block

    def valid_block(self, new_block, last_block) :
        merkle_newBlock_transaction = MerkleTree(new_block['block']['blockData'])
        merkle_newBlock_smartcontact = MerkleTree(self.current_smartcontracts.return_hashList())
        if new_block['block']['blockHeader']['index'] - 1 != last_block['block']['blockHeader']['index'] :
            return False
        elif  (new_block['block']['blockHeader']['timestamp'] < last_block['block']['blockHeader']['timestamp'] - 60  
             or new_block['block']['blockHeader']['timestamp'] - 60  > time.time() ):
            return False
        elif new_block['block']['blockHeader']['transactions_hash'] != merkle_newBlock_transaction.get_root() :
            return False
        elif new_block['block']['blockHeader']['smrtcontract_hash'] != merkle_newBlock_smartcontact.get_root() :
            return False
        elif new_block['block']['blockHeader']['previous_hash'] != last_block['blockHash'] :
            return False
        
        return True

    def push_block(self, new_block) :
        if self.valid_block(new_block, self.last_block) == False :
            return -1
        self.chain.append(new_block)
        self.current_transactions = self.current_transactions.reset_transaction_all()
        return len(self.chain)
    
    def is_chain_valid(self, chain):           
        last_block = chain['chain'][0]
        current_index = 1

        while current_index < len(chain): 
            block = chain[current_index]
            if self.valid_block(block, last_block) == False :
                return False
            last_block = block
            current_index += 1
            
        return True
   
