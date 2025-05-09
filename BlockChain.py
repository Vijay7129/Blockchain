import hashlib
import time
import json

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()  # Compute hash after setting all attributes

    def calculate_hash(self):
        # Only include the necessary fields, not the hash itself
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Mining: adjust nonce until hash starts with n zeros
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Adjust difficulty as needed

    def create_genesis_block(self):
        return Block(0, str(time.time()), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=str(time.time()),
            data=data,
            previous_hash=latest_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # Check if stored hash is still valid
            if curr.hash != curr.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False

            # Check if previous hash matches
            if curr.previous_hash != prev.hash:
                print(f"Invalid previous hash at block {i}")
                return False

        return True

# --- Usage Example ---
if __name__ == "__main__":
    my_blockchain = Blockchain()
    
    my_blockchain.add_block({"sender": "Alice", "receiver": "Bob", "amount": 50})
    my_blockchain.add_block({"sender": "Bob", "receiver": "Charlie", "amount": 50})
    
    # Print all block details
    for block in my_blockchain.chain:
        print(json.dumps(vars(block), indent=4))
    
    print("Blockchain valid?", my_blockchain.is_chain_valid())
