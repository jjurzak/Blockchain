import hashlib
import time 
import json
import requests
from urllib.parse import non_hierarchical, urlparse

class Blockchain:
    def __init__(self):
        self.jj_chain = []
        self.jj_create_genesis_block()
        self.jj_mempool = []
        self.nodes = set()


    def jj_create_genesis_block(self):
        jj_previous_hash = "Jurzak"
        jj_nonce = 59099
        jj_block = {
            "index": 0,
            "timestamp": time.time(),
            "transactions": [],
            "merkle_root": None,
            "data": "Genesis Block",
            "previous_hash": jj_previous_hash,
            "nonce": jj_nonce,
            "hash": self.jj_calculate_hash(0, time.time(), "Genesis Block", jj_previous_hash, jj_nonce)
                }
        self.jj_chain.append(jj_block)

    def jj_calculate_hash(self, index, timestamp, data, previous_hash, nonce):
        jj_block_string = f"{index}{timestamp}{data}{previous_hash}{nonce}"
        return hashlib.sha256(jj_block_string.encode()).hexdigest()

    def jj_get_last_block(self):
        return self.jj_chain[-1]

       
    def jj_add_transaction_to_mempool(self, sender, recipient, amount):
        tx = {
            "sender": sender,
            "recipient": recipient, 
            "amount": amount,
        }
        self.jj_mempool.append(tx)
        return len(self.jj_chain)

    def jj_hash_transaction(self, tx):
        tx_str = json.dumps(tx, sort_keys=True).encode()
        return hashlib.sha256(tx_str).hexdigest()

    def jj_merkle_root(self, transactions):
        if not transactions:
            return None

        level = [self.jj_hash_transaction(tx) for tx in transactions]
        
        while len(level) > 1:
            if len(level) % 2 != 0:
                level.append(level[-1])

            new_level = []
            for i in range(0, len(level), 2):
                combined = (level[i] + level[i+1]).encode()
                new_hash = hashlib.sha256(combined).hexdigest()
                new_level.append(new_hash)

            level = new_level

        return level[0]
    
    def jj_mine_block(self, difficulty):
        last_block = self.jj_get_last_block()

        index = len(self.jj_chain)
        timestamp = time.time()
        transactions = list(self.jj_mempool)
        previous_hash = last_block["hash"]
        nonce = 0

        merkle_root = self.jj_merkle_root(transactions)

        while True:
            block_hash = self.jj_calculate_hash(index, timestamp, transactions, previous_hash, nonce)
            if block_hash.startswith("0" * difficulty):
                break
            nonce += 1

        new_block = {
                "index": index,
                "timestamp": timestamp,
                "transactions": transactions,
                "merkle_root": merkle_root,
                "previous_hash": previous_hash,
                "nonce": nonce,
                "hash": block_hash
                }

        self.jj_chain.append(new_block)
        self.jj_mempool = []

        return new_block
    
    def jj_register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Nieprawidlowy adres url')

    def jj_valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block['previous_hash'] != last_block['hash']:
                return False
            
            recalculated_hash = self.jj_calculate_hash(
                    block['index'],
                    block['timestamp'],
                    block['transactions'],
                    block['previous_hash'],
                    block['nonce']
                    )
            if block['hash'] != recalculated_hash:
                return False

            if not block['hash'].startswith('0000'):
                return False
            
            last_block = block
            current_index += 1

        return True

    def jj_resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None 
        max_length = len(self.jj_chain)

        for node in neighbours:
            try:
                response = requests.get(f'http://{node}/chain')

                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    if length > max_length and self.jj_valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except requests.exceptions.RequestException:
                continue

        if new_chain:
            self.jj_chain = new_chain
            return True

        return False


     
    def jj_add_block(self, data, difficulty):
        last_block = self.jj_get_last_block()
        index = len(self.jj_chain)
        timestamp = time.time()
        previous_hash = last_block["hash"]
        nonce = 0

    
        print(f"Szukanie poprawnego hasha dla #{index}")

        start_time = time.time()

        while True:
            new_hash = self.jj_calculate_hash(index, timestamp, data, previous_hash, nonce)
            if new_hash.startswith("0" * difficulty) and new_hash.endswith("09"):
                end_time = time.time()
                eta = end_time - start_time
                print(f"Znaleziono hash: {new_hash}")
                print(f"Nonce: {nonce}")
                print(f"Czas szukania: {eta:.4f} sek")
                break
            nonce += 1

        new_block = {
                "index" : index,
                "timestamp" : timestamp,
                "data" : data,
                "previous_hash" : previous_hash,
                "nonce": nonce,
                "hash" : new_hash,
        }

        self.jj_chain.append(new_block)

    def jj_display_chain(self):
        for block in self.jj_chain:
            print("\nBlok:")
            for key, value in block.items():
                print(f"{key}: {value}")

if __name__ == "__main__":
    blockchain = Blockchain()
    
 
    blockchain.jj_add_block("Drugi blok", difficulty=3)
    
    blockchain.jj_add_block("Trzeci blok", difficulty=4)

    blockchain.jj_add_block("Trzeci blok", difficulty=5)
    

    blockchain.jj_display_chain()
