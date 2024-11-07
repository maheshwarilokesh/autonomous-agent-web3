# Core Agent structure 
import asyncio
import random
import time
from web3 import Web3
from threading import Thread

# Sample words 
WORDS = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]

# Message structure
class Message:
    def __init__(self, content):
        self.content = content
        self.timestamp = time.time()
    
    def __str__(self):
        return f"Message(content='{self.content}', timestamp={self.timestamp})"

# Autonomous Agent
class AutonomousAgent:
    def __init__(self, eth_provider, contract_address, source_address, target_address, private_key):
        self.inbox = asyncio.Queue()
        self.outbox = asyncio.Queue()
        self.handlers = {}
        self.behaviors = []

        self.web3 = Web3(Web3.HTTPProvider(eth_provider))
        self.contract_address = contract_address
        self.source_address = source_address
        self.target_address = target_address
        self.private_key = private_key
        self.contract = self.load_contract()
        print("AutonomousAgent started")

    def load_contract(self):
        # ERC20 ABI
        abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"transferAndCall","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"typeAndVersion","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"}]'  # Replace with actual ABI
        return self.web3.eth.contract(address=self.contract_address, abi=abi)

    async def run(self):
        # Start behaviors and handlers
        for behavior in self.behaviors:
            asyncio.create_task(behavior())
            print(f"Behavior {behavior.__name__} started.")
        while True:
            message = await self.inbox.get()
            print(f"Processing message from inbox: {message}")
            await self.process_message(message)

    def register_handler(self, keyword, handler):
        self.handlers[keyword] = handler
        print(f"Handler registered for keyword '{keyword}'.")

    def register_behavior(self, behavior):
        self.behaviors.append(behavior)
        print(f"Behavior '{behavior.__name__}' registered.")

    async def process_message(self, message):
        for keyword, handler in self.handlers.items():
            if keyword in message.content:
                print(f"Handler for '{keyword}' triggered by message: {message}")
                await handler(message)

    async def send_message(self, message):
        await self.outbox.put(message)
        print(f"Message sent to outbox: {message}")

    async def random_message_generator(self):
        while True:
            word1, word2 = random.sample(WORDS, 2)
            message_content = f"{word1} {word2}"
            message = Message(message_content)
            await self.send_message(message)
            await self.inbox.put(message)
            print(f"Generated random message: {message}")
            await asyncio.sleep(2)

    async def check_token_balance(self):
        while True:
            balance = self.get_erc20_balance(self.source_address)
            print(f"Checked ERC-20 Token Balance: {balance}")
            await asyncio.sleep(10)

    def get_erc20_balance(self, address):
        balance = self.contract.functions.balanceOf(address).call()
        print(balance)
        return self.web3.from_wei(balance, 'ether')
        # return balance

    async def hello_handler(self, message):
        print(f"Received 'hello' message: {message.content}")

    async def crypto_transfer_handler(self, message):
        print(f"'crypto' handler triggered by message: {message.content}")
        if self.get_erc20_balance(self.source_address) >= 1:
            tx_hash = self.transfer_erc20_token(self.target_address, 1)
            print(f"Transfer of 1 token initiated, transaction hash: {tx_hash}")
        else:
            logging.warning("Insufficient balance for transfer.")

    def transfer_erc20_token(self, to_address, amount):
        nonce = self.web3.eth.get_transaction_count(self.source_address, 'pending')
        tx = self.contract.functions.transfer(to_address, self.web3.to_wei(amount, 'ether')).build_transaction({
            'from': self.source_address,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash.hex()
