import json
from Network_cyper1 import MerkleTree, hash

class Smartcontract() :
    def __init__(self) :
        self.smartcontracts_list = []
        self.smartcontracts_listHash = []

    def new_smartcontracts_list(self, transaction) :
        contracts_list = {
            "type" : transaction["smartcontract_type"],
            "smartcontracts" : []
        }
        contracts_hash = {
            "type" : transaction["smartcontract_type"],
            "hash" : None
        }
        self.smartcontracts_list.append(contracts_list)
        self.smartcontracts_listHash.append(contracts_hash)
        return self.smartcontracts_list[-1]
    
    def new_smartcontract(self, smartcontract) :
        for i, list in enumerate(self.smartcontracts_list) :
            if list["type"] == smartcontract["smartcontract_type"] :
                address = hash(smartcontract)
                smartcontract["smartcontract_address"] = address
                self.smartcontract_list[i]["smartcontracts"].append(smartcontract)
                self.smartcontracts_listHash = self.update_smartcontract_hash(smartcontract["smartcontract_type"])
                return self.smartcontracts_list[i]["smartcontracts"][-1]
    
    def update_smartcontract(self, smartcontract):
        for i, list in enumerate(self.smartcontracts_list) :
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
            
    def return_hashList(self) :
        hash_list = []
        for hash_dic in self.smartcontracts_listHash :
            hash_list.append(hash_dic["hash"])
        return hash_list
    
class Transaction() :
    def __init__(self) :
        self.transaction = []
        self.transaction_hash = None
    
    def new_transaction(self, transaction):
        self.transaction.append(transaction)
        self.transaction_hash = MerkleTree(self.transaction).get_root()
        return self.transaction[-1]
    
    def get_transaction_hash(self) :
        return self.transaction_hash
    
    def get_transaction(self) :
        return self.transaction
    
    def reset_transaction_all(self) :
        self.transaction = []
        self.transaction_hash = None
        return self.transaction
    
class VirualMachine() :
    def __init__(self, name) :
        self.VM_address = name
        
    def ExeSmartcontract(self, smartcontract_list, transaction) :
        for smartcontract_types in smartcontract_list :
            if smartcontract_types["type"] == transaction["smartcontract"]["smartcontract_type"] :
                for smartcontract in smartcontract_types["smartcontracts"] :
                    if smartcontract["smartcontract_address"] == transaction["smartcontract"]["smartcontract_address"] :
                        exec(smartcontract["smartcontract_data"])
                        exec(smartcontract["smartcontract_code"])
                        exec(transaction["smartcontract"]["request"])
        return True