import unittest
import asyncio
from agent import AutonomousAgent, Message
from config import eth_provider, contract_address, source_address, target_address, private_key

class TestAutonomousAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AutonomousAgent(eth_provider, contract_address, source_address, target_address, private_key)
        self.agent.register_handler("hello", self.agent.hello_handler)
    
    def test_hello_handler(self):
        message = Message("hello world")

        async def run_test():
            await self.agent.inbox.put(message) 
            await self.agent.process_message(message)

        asyncio.run(run_test())

        self.assertIn("hello", message.content)

if __name__ == "__main__":
    unittest.main()
