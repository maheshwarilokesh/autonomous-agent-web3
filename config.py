# File to load env variables in the application
import os
from dotenv import load_dotenv

load_dotenv()

eth_provider = os.getenv("RPC_NODE_URL")
contract_address = os.getenv("ERC20_TOKEN_ADDRESS")
source_address = os.getenv("SOURCE_ADDRESS")
target_address = os.getenv("RECEIVER_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")