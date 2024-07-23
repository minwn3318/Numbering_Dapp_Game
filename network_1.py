import hashlib 
import json
import time
import random
import requests
from flask import Flask, request, jsonify
from urllib.parse import urlparse

class Blockchain(object):
    
    def __init__(self, account_weight, account_name):
        self.chain = []                                   
        self.current_transaction = []                     
        self.nodes = set()                                
        self.miner_wallet = {'account_name': account_name, 'weight': account_weight}  
        self.new_block(previous_hash='genesis_block', address = account_name)        
        self.account_name = account_name
        self.account_weight = account_weight

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha256(block_string).hexdigest()   
    
    @property
    def last_block(self):
        return self.chain[-1]                             

    @property
    def get_nodeList(self) :
        node_list = []
        for node in self.nodes :
            node_list.append(node)
        return node_list
    
    @property
    def get_transaction(self):
        return  len(self.current_transaction)                

    def pos(self):
        winner_list = []            
        time.sleep(1)
        my_winner = self.pick_winner(account_name = self.account_name, account_weight = self.account_weight)   
        winner_list.append(my_winner)   
        time.sleep(1)

        for target_node in blockchain.nodes:             
            print("self pos : ",target_node)
            headers = {'Content-Type' : 'application/json; charset=utf-8'}
            res = requests.get('http://' + target_node   + "/nodes/pick_winner", headers=headers)
            winner_info = json.loads(res.content)  
            print(winner_info)
            winner_list.append(winner_info['winner']) 

        final_winner = max(winner_list,key = winner_list.count)  
        print("final_winner selected : ", final_winner)
        
        return final_winner


    def pick_winner(self,account_name, account_weight):  
        candidate_list = []  
             
        for w in range(account_weight):  
            print('self 5000 :', w)
            candidate_list.append(account_name)
       
        random.shuffle(candidate_list)       
        for x in  candidate_list:           
            winner  = x
            print("WINNER SELECTED 5000: ", winner)
            break
        
        return winner                       

    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append(
            {
                'sender' : sender, 
                'recipient' : recipient, 
                'amount' : amount,
                'timestamp':time.time()
            }
        )
        return self.last_block['index'] + 1   

    def new_block(self, previous_hash=None, address = ''):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : time.time(), # timestamp from 1970
            'transactions' : self.current_transaction,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
            'validator' : address
        }
        block["hash"] = self.hash(block)
        self.current_transaction = []
        self.chain.append(block)     
        return block

    def is_chain_valid(self, chain):           
        last_block = chain['chain'][0]
        current_index = 1

        while current_index < len(chain): 
            block = chain[current_index]
            print('%s' % last_block)
            print('%s' % block)
            print("\n--------\n")
            if block['previous_hash'] != self.hash(last_block):
                return False
            last_block = block
            current_index += 1
            
        return True
    
    def register_node(self, address): 
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc) 
        
        
    def resolve_conflict(self):    
        
        for registering_node in blockchain.nodes:            
            headers = {'Content-Type' : 'application/json; charset=utf-8'}
            print(registering_node,  '    /http://' + registering_node   + "/chain")
            res = requests.get('http://' + registering_node   + "/chain", headers=headers)
            target_node_info = json.loads(res.content)
            
            
            if target_node_info['length'] > len(self.chain):  
                if self.is_chain_valid(target_node_info):     
                    self.blockchain = target_node_info        
                    return
        return     
        
my_ip = '127.0.0.1'
my_port = '5000'
node_identifier = 'node_'+my_port
mine_owner = 'master001'
mine_profit = 0.1

blockchain = Blockchain(account_name=mine_owner, account_weight= 2)

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    print("chain info requested!!")
    response = {
        'chain' : blockchain.chain, 
        'length' : len(blockchain.chain), 
    }
    return jsonify(response), 200

@app.route('/transaction', methods = ['GET'])
def full_transaction():
    print("transaction info requested!!")
    response = {
        'transaction' : blockchain.current_transaction,
        'length' : blockchain.get_transaction
    }
    return jsonify(response), 200

@app.route('/nodeList', methods = ['GET'])
def full_nodeList():
    print(" info requested!!")
    respones = {
        'node_list' : blockchain.get_nodeList,
        'length' : len(blockchain.get_nodeList)
    }
    return jsonify(respones), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json() 
    print("transactions_new!!! : ", values)
    required = ['sender', 'recipient', 'amount'] 

    if not all(k in values for k in required):
        print('error')
        return 'missing values', 400

    index = blockchain.new_transaction(values['sender'],values['recipient'],
values['amount'])
        
    response = {'message' : 'Transaction will be added to Block {%s}' % index}

    if "type" not in values:  
        for node in blockchain.nodes:  
            headers = {'Content-Type' : 'application/json; charset=utf-8'}
            data = {
                "sender": values['sender'],
                "recipient": values['recipient'],
                "amount": values['amount'],
                "type" : "sharing"   
            }
            requests.post("http://" + node  + "/transactions/new", headers=headers, data=json.dumps(data))
            print("share transaction to >>   ","http://" + node )
            
    return jsonify(response), 201

@app.route('/block/new', methods=['POST'])
def new_block():
    block = request.get_json() 
    print("NEW BLOCK  ADDED!!! : ", block)
    
    blockchain.current_transaction = []
    blockchain.chain.append(block) 
    response = {'message' : 'Transaction will be added to Block {%s}' % block['index']}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    transaction_len = blockchain.get_transaction
    if transaction_len == 0 :
        response = {
            'message' : 'No transaction in node. Need making transaction ',
            'transactions length' : transaction_len
        }
        return jsonify(response), 200
    
    print("MINING STARTED")   
    final_winner = blockchain.pos()  

    if final_winner == blockchain.account_name:  
        print("MY NODE IS SELECTED AS MINER NODE")
        blockchain.new_transaction(           
            sender="mining_profit", 
            recipient=final_winner, 
            amount=mine_profit, # coinbase transaction  
        )

        previous_hash = blockchain.hash(blockchain.chain[-1])
        block = blockchain.new_block(previous_hash = previous_hash, address = final_winner)  
        print(final_winner," IS SELECTED AS MINER NODE")

        for node in blockchain.nodes: 
            headers = {'Content-Type' : 'application/json; charset=utf-8'}
            alarm_newBlock = requests.post("http://" + node  + "/block/new", headers=headers, data = json.dumps(blockchain.chain[-1] ) ) 
            print(alarm_newBlock.content)

        response = {
            'message' : 'new block found',
            'index' : block['index'],
            'transactions' : block['transactions'],
            'validator' : block['validator'],
            'previous_hash' : block['previous_hash'],
            'hash' : block['hash']
        }
    
    else : 
        print("MY NODE IS NOT SELECTED AS MINER NODE")
 
    response = {'message' : 'Mining Complete'}
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json() 
    print("register nodes !!! : ", values)
    registering_node =  values.get('nodes')
    if registering_node == None:  
        return "Error: Please supply a valid list of nodes", 400
     
    if registering_node.split("//")[1] in blockchain.nodes:
        print("Node already registered")  
        response = {
            'message' : 'Already Registered Node',
            'total_nodes' : list(blockchain.nodes),
        }

    else:  
        blockchain.register_node(registering_node) 
        
        headers = {'Content-Type' : 'application/json; charset=utf-8'}
        data = {
            "nodes": 'http://' + my_ip + ":" + my_port
        }
        print("MY NODE INFO " , 'http://' + my_ip + ":" + my_port)
        requests.post( registering_node + "/nodes/register", headers=headers, data=json.dumps(data))
        
        for add_node in blockchain.nodes:
            if add_node != registering_node.split("//")[1]:
                print('add_node : ', add_node)
                headers = {'Content-Type' : 'application/json; charset=utf-8'}
                data = {
                    "nodes": registering_node
                }
                requests.post('http://' + add_node   + "/nodes/register", headers=headers, data=json.dumps(data))

        response = {
            'message' : 'New nodes have been added',
            'total_nodes' : list(blockchain.nodes),
        }
    return jsonify(response), 201

@app.route('/nodes/node_weight', methods=['GET'])
def node_weight():
    print("node_weight requested!!")

    response = {
        'account_name' : blockchain.account_name,
        'account_weight' : blockchain.account_weight
    }
    return jsonify(response), 200    

    
@app.route('/nodes/pick_winner', methods=['GET'])
def pick_winner():
    print("pick_winner requested!!")
    
    candidate_list = []  
    for w in range(blockchain.account_weight): 
        candidate_list.append(blockchain.account_name)

    for target_node in blockchain.nodes:                    
        headers = {'Content-Type' : 'application/json; charset=utf-8'}
        res = requests.get('http://' + target_node   + "/nodes/node_weight", headers=headers)
        target_node_info = json.loads(res.content)
                
        for repeated in range(target_node_info['account_weight']):
            candidate_list.append(target_node_info['account_name'])

    random.shuffle(candidate_list)       
    for x in  candidate_list:           
        winner  = x
        break

    
    response = {
        'winner' : winner, 
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host=my_ip, port=my_port)