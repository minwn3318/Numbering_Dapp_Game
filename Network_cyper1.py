import hashlib 
import math
import json

def hash(block):
    block_string = json.dumps(block, sort_keys=True).encode() 
    return hashlib.sha256(block_string).hexdigest() 

class MerkleTree:
    def __init__(self, data_blocks):
        self.leaves = [hash(data) for data in data_blocks]
        self.tree = self.build_tree(self.leaves)
    
    def build_tree(self, leaves):
        tree = [leaves]
        while len(leaves) > 1:
            if len(leaves) % 2 == 1:
                leaves.append(leaves[-1])  # 홀수 개일 경우 마지막 원소를 복제
            leaves = [hash(leaves[i] + leaves[i+1]) for i in range(0, len(leaves), 2)]
            tree.append(leaves)
        return tree

    def get_root(self):
        return self.tree[-1][0] if self.tree else None
    
    def get_proof(self, index):
        proof = []
        for level in self.tree[:-1]:
            pair_index = index ^ 1
            proof.append(level[pair_index])
            index //= 2
        return proof
    
    def verify_proof(self, proof, target_hash, root_hash):
        current_hash = target_hash
        for sibling_hash in proof:
            if current_hash < sibling_hash:
                current_hash = hash(current_hash + sibling_hash)
            else:
                current_hash = hash(sibling_hash + current_hash)
        return current_hash == root_hash