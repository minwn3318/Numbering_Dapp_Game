import json
import time
import random
import requests

from Network_http1 import node_list
from Network_cyper1 import MerkleTree, hash

class Smartcontract_container() :
    def __init__(self) :
        self.smartcontracts_list = []
        self.smartcontracts_listHash = []

    def new_smartcontracts_list(self, transaction) :
        new_contracts_list = {
            "type" : transaction["smartcontract_type"],
            "smartcontracts" : []
        }
        new_contracts_hash = {
            "type" : transaction["smartcontract_type"],
            "hash" : None
        }
        self.smartcontracts_list.append(new_contracts_list)
        self.smartcontracts_listHash.append(new_contracts_hash)
        return self.smartcontracts_list[-1]
    
    def new_smartcontract(self, smartcontract) :
        for i, list in enumerate(self.smartcontracts_list) :
            if list["type"] == smartcontract["smartcontract_type"] :
                new_smartcontract = {
                    "smartcontract_type" : smartcontract["smartcontract_type"],
                    "smartcontract_data" : smartcontract["smartcontract_data"],
                    "smartcontract_play" : smartcontract["smartcontract_play"],
                    "smartcontract_signature" : smartcontract["smartcontract_signature"]
                }
                address = hash(new_smartcontract)
                new_smartcontract["smartcontract_address"] = address
                self.smartcontract_list[i]["smartcontracts"].append(new_smartcontract)
                self.smartcontracts_listHash = self.update_smartcontract_hash(new_smartcontract)
                return self.smartcontracts_list[i]["smartcontracts"][-1]
    
    def update_smartcontract(self, smartcontract):
        for i, list in enumerate(self.smartcontracts_list) :
            if smartcontract["smartcontract_type"] == list["type"] :
                for j, contract in enumerate(list["smartcontracts"]) :
                    if contract["smartcontract_address"] == smartcontract["smartcontract_address"] :
                        self.smartcontracts_list[i][j] = smartcontract
                        return  self.smartcontracts_list[i][j]

    def update_smartcontract_hash(self, type) :
        for i, list in enumerate(self.smartcontracts_list) :
            if list["type"] == type :
                merkle = MerkleTree(self.smartcontracts_list[i]["smartcontracts"])
                self.smartcontracts_listHash[i]["hash"] = merkle.get_root()
                return self.smartcontracts_listHash
    
    def return_smartcontract_container(self) :
        return self.smartcontracts_list

    def return_hashList(self) :
        hash_list = []
        for hash_dic in self.smartcontracts_listHash :
            hash_list.append(hash_dic["hash"])
        return hash_list
    
    def valid_smartcontract_data(self, target_smartcontract_data, recive_smartcontract_data) :
        if target_smartcontract_data["metaData"] != recive_smartcontract_data["metaData"] :
            return False
        elif target_smartcontract_data["claim"] != recive_smartcontract_data["claim"] :
            return False
        elif target_smartcontract_data["signature"] != recive_smartcontract_data["signature"] :
            return False
        return True
 
class Transaction_container() :
    def __init__(self) :
        self.transaction_container = []
        self.transaction_hash = None
    
    def new_transaction(self, transaction):
        if self.valid_transaction(transaction) == False :
            return {"message" : "error"}
        newer_trnansaction = {
            "sender" : transaction["sender"],
            "recipient" : transaction["recipient"],
            "transaction_type" : transaction["transaction_type"],
            "transaction_data" : transaction["transaction_data"],
            "transaction_play" : transaction["transaction_play"],
        }
        self.transaction_container.append(newer_trnansaction)
        self.transaction_hash = MerkleTree(self.transaction_container).get_root()
        return self.transaction_container[-1]
    
    def get_transaction_hash(self) :
        return self.transaction_hash
    
    def get_transaction_container(self) :
        return self.transaction_container
    
    def reset_transaction_all(self) :
        self.transaction_container = []
        self.transaction_hash = None
        return self.transaction
    
    def change_transaction(self, new_transactionList) :
        self.transaction_container = new_transactionList
        return self.transaction_container

    def valid_transaction(self, recive_transaction) :
        valid_keys = ["sender", "recipient", "transaction_type", "transaction_data", "transaction_play"]
        for key in valid_keys:
            if key not in recive_transaction:
                return False
        return True 

def ExeSmartcontract(smartcontract_container, transaction) :
    smartcontract_list = smartcontract_container.return_smartcontract_container()
    for smartcontract_types in smartcontract_list :
        if smartcontract_types["type"] == transaction["transaction_play"]["smartcontract_type"] :
            for smartcontract in smartcontract_types["smartcontracts"] :
                if smartcontract["smartcontract_address"] == transaction["transaction_play"]["smartcontract_address"] :
                    if smartcontract_container.valid_smartcontract_data() == False :
                        return {"message" : "error"}
                    get_data = {}
                    return_data = {
                        "sender" : sender,
                        "recipient" : recipient,
                        "transaction_type" : transaction_type,
                        "transaction_data" : transaction_data,
                        "transaction_play" : transaction_play
                    }
                    exec(smartcontract["smartcontract_data"])
                    exec(smartcontract["smartcontract_code"])
                    exec(transaction["tranasction_data"], get_data)
                    exec(transaction["tranasction_play"], get_data, return_data)
                    return_data["timestampe"] = time.time()
                    headers = {'Content-Type' : 'application/json; charset=utf-8'}
                    random.shuffle(node_list)
                    node = node_list[0]
                    requests.post("https://127.0.0.1:"+str(node)+"/node/transaction", headers=headers, return_data=json.dumps(return_data))
                    return return_data