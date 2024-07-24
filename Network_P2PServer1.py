import requests
import random
import websockets
import asyncio
from urllib.parse import urlparse

from Network_cyper1 import hash, MerkleTree
from Network_node1 import blockchain
from Network_VM1 import Smartcontract_container, Transaction_container, ExeSmartcontract
from Network_http1 import mine_owner

my_ip = '127.0.0.1'
my_port = 6000

connected_peers = set()
messageType = ["transaction","requestTransaction", "requestBlock", "requestChain", "requestMineOwner", "requestPOS",
               "responseTransaction", "responseBlocks", "responseMineOwner", "responsePOS"]

def send_transaction(transaction) :
    msg = {
        "messageType" : messageType[0],
        "data" : transaction
    }
    return msg

def send_copy(transaction) :
    msg ={
        "messageType" : messageType[1],
        "data" : transaction
    }
    return msg

def request_allTransaction() :
    msg = {
        "messageType" : messageType[1],
        "data" : None
    }

def request_oneBlockMsg() :
    msg = {
        "messageType" : messageType[2],
        "data" : None
    }
    return msg

def request_allChainMsg() :
    msg = {
        "messageType" : messageType[3],
        "data" : None
    }
    return msg

def request_mineOwner() :
    msg = {
        "messageType" : messageType[4],
        "data" : None
    }
    return msg

def request_POS():
    msg = {
        "messageType" : messageType[5],
        "data" : None
    }
    return msg

def send_allTransaction() :
    msg = {
        "mesageType" : messageType[6],
        "data" : blockchain.transaction
    }
    return msg

def send_oneBlockMsg() :
    msg = {
        "messageType" : messageType[7],
        "data" : blockchain.last_block
    }
    return msg

def send_allChainMsg() :
    msg = {
        "messageType" : messageType[7],
        "data" : blockchain.all_chain
    }
    return msg

def send_mineOwner() :
    msg = {
        "messageType" : messageType[8],
        "data" : mine_owner
    }
    return msg

def send_POS(winner):
    msg={
        "messageType" : messageType[9],
        "data" : winner
    }
    return msg
def handleblocks(block) :
    pass

async def pos(websocket = None):
    candidate_list = []
    for w in range(mine_owner["owner_pointAddress"]) :
        candidate_list.append(mine_owner["owner_wallet"])

    candidate_data = request_mineOwner()
    async for peer in connected_peers :
        await peer.send(candidate_data)
        response = await peer.recv()
        candidate_list.append(response)
    random.shuffle(candidate_list)
    winner = candidate_list[0]
    return winner

async def pick_winner(winner_list) :
    new_data = request_POS()
    async for peer in connected_peers :
        await peer.send(new_data)
        response = await peer.recv()


async def message_handler(websocket, path):
    # 피어 연결 시 처리
    connected_peers.add(websocket)
    try:
        async for message in websocket:
            if message["messageType"] == messageType[0] :
                if not message["data"] in blockchain.current_transactions:
                    blockchain.new_transaction(message["data"])
                    await broadcast(message, websocket)

            elif message["messageType"] == messageType[1] :
                new_message = send_oneBlockMsg()
                await websocket.send(new_message)
                
            elif message["messageType"] == messageType[2] :
                new_message = send_allChainMsg()
                await websocket.send(new_message)
                
            elif message["messageType"] == messageType[3] :
                new_message = send_allTransaction()
                await websocket.send(new_message)
                
            elif message["messageType"] == messageType[4] :
                new_message = send_mineOwner()
                await websocket.send(new_message)
                
            elif message["messageType"] == messageType[5] :
                pos(websocket)

            elif message["messageType"] == messageType[6] :
                blockchain.chang_CurrentTran(message["data"])

            elif message["messageType"] == messageType[7] :
                handleblocks()

            elif message["messageType"] == messageType[8] :
                pass

    finally:
        connected_peers.remove(websocket)

async def broadcast(message, sender):
    for peer in connected_peers:
        if peer != sender:
            await peer.send(message)

async def start_server():
    server = await websockets.serve(message_handler, "localhost", my_port)
    await server.wait_closed()

async def connect_to_peer(uri):
    async with websockets.connect(uri) as websocket:
        message = request_allChainMsg()
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Received response: {response}")

async def main():
    # 서버 시작
    server_task = asyncio.create_task(start_server())

    # 클라이언트 연결
    await asyncio.sleep(1)  # 서버가 시작될 시간을 줌
    client_task = asyncio.create_task(connect_to_peer('ws://localhost:8765'))

    await asyncio.gather(server_task, client_task)