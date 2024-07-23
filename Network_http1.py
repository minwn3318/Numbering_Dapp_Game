from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse
import json
from Network_node1 import Blockchain, MerkleTree

my_ip = '127.0.0.1'
my_port = '5000'
node_identifier = 'node_'+my_port
mine_owner = {
    'owner_wallet' : None,
    'owner_pointAddress' : None, 
}

blockchain = Blockchain()
node_list = []
app = Flask(__name__)

headers = {'Content-Type' : 'application/json; charset=utf-8'}

@app.route('/chain', methods=['GET'])
def full_chain():
    print("chain info requested!!")
    response = {
        'chain' : blockchain.chain, 
        'length' : len(blockchain.chain), 
    }
    return jsonify(response), 200

@app.route('/access_Blockchain', methods = ['POST'])
def register_wallet() :
    value = request.get_json()
    mine_owner['owner_wallet'] = value.get('account')
    mine_owner['owner_pointAddress'] = value.get('point')

    response = mine_owner
    return jsonify(response), 201

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
            'total_nodes' : node_list,
        }

    else:  
        parseURL = urlparse(registering_node)
        node_list.append(parseURL.netloc)
        
        data = {
            "nodes": 'http://' + my_ip + ":" + my_port
        }
        print("MY NODE INFO " , 'http://' + my_ip + ":" + my_port)
        requests.post( registering_node + "/nodes/register", headers=headers, data=json.dumps(data))
        
        for add_node in node_list:
            if add_node != registering_node.split("//")[1]:
                print('add_node : ', add_node)
                data = {
                    "nodes": registering_node
                }
                requests.post('http://' + add_node   + "/nodes/register", headers=headers, data=json.dumps(data))

        response = {
            'message' : 'New nodes have been added',
            'total_nodes' : node_list,
        }

    return jsonify(response), 201

@app.route('/new/transaction', methods = ['POST'])
def new_transaction() :
    value = request.get_json()
    blockchain.new_transaction(value)
    respone = {"type" : "Sussec new/transaction"}
    return jsonify(respone), 201

@app.route('/new/smartcontract', methods = ['POST'])
def new_smartcontract() :
    value = request.get_json()
    blockchain.new_smartcontract()
    response = {"type" : "Sussec new/smartcontract"}
    return jsonify(response), 201

@app.route('/mine', methods = ['POST'])
def mine() :
    return jsonify(), 201