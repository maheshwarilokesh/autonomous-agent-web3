import unittest
import asyncio
from agent import AutonomousAgent, Message
from config import eth_provider, contract_address, source_address, target_address, private_key

class TestAgentCommunication(unittest.TestCase):
    def setUp(self):
        self.agent1 = AutonomousAgent(eth_provider, contract_address, source_address, target_address, private_key)
        self.agent2 = AutonomousAgent(eth_provider, contract_address, source_address, target_address, private_key)
        
        self.agent1.outbox = self.agent2.inbox
        self.agent2.outbox = self.agent1.inbox

    def test_inter_agent_communication(self):
        message_from_agent1 = Message("crypto transfer")
        asyncio.run(self.agent1.outbox.put(message_from_agent1))
        
        received_message = asyncio.run(self.agent2.inbox.get())
        self.assertEqual(received_message.content, message_from_agent1.content)

if __name__ == "__main__":
    unittest.main()
