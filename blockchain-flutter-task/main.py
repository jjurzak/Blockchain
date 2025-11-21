import hashlib
import time 
import json

class Blockchain:
    def __init__(self):
        self.jj_chain = []
        self.jj_create_genesis_block()
        self.jj_mempool = []


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
