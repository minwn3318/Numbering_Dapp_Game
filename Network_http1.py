from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse
import json
from Network_node1 import blockchain
from Network_VM1 import MerkleTree

my_ip = '127.0.0.1'
my_port = '5000'
node_identifier = 'node_'+my_port
mine_owner = {
    'owner_wallet' : None,
    'owner_pointAddress' : None, 
}

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
def register_nodes() :
    pass

@app.route('/new/transaction', methods = ['POST'])
def new_transaction() :
    value = request.get_json()
    respone = blockchain.new_transaction(value)
    respone["message"] = "Sussec new/transaction"
    return jsonify(respone), 201

@app.route('/mine', methods = ['POST'])
def mine() :
    return jsonify(), 201