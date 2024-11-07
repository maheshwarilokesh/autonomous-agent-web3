# Run the agent and set handlers and behaviors
import asyncio
from threading import Thread
from agent import AutonomousAgent
from config import eth_provider, contract_address, source_address, target_address, private_key

# Instantiate two agents
agent1 = AutonomousAgent(eth_provider, contract_address, source_address, target_address, private_key)
agent2 = AutonomousAgent(eth_provider, contract_address, source_address, target_address, private_key)

# Link outbox to inbox
agent1.outbox = agent2.inbox
agent2.outbox = agent1.inbox

# Register behaviors and handlers for both agents
agent1.register_behavior(agent1.random_message_generator)
agent1.register_behavior(agent1.check_token_balance)
agent1.register_handler("hello", agent1.hello_handler)
agent1.register_handler("crypto", agent1.crypto_transfer_handler)

agent2.register_behavior(agent2.random_message_generator)
agent2.register_behavior(agent2.check_token_balance)
agent2.register_handler("hello", agent2.hello_handler)
agent2.register_handler("crypto", agent2.crypto_transfer_handler)

async def main():
    await asyncio.gather(agent1.run(), agent2.run())
    
thread1 = Thread(target=lambda: asyncio.run(main()))
thread1.start()