## Getting started

To make it easy for you to get started with Github, here's a list of recommended next steps.


## Installation

To install and run the Pipeline APIs, follow these steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/maheshwarilokesh/autonomous-agent-web3.git
   ```

2. Create a virtual environment:

   ```shell
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   - On macOS and Linux:

     ```shell
     source venv/bin/activate
     ```

4. Install the required dependencies:

   ```shell
   pip3 install -r requirements.txt
   ```

5. Configuration:
    
   - Create a `.env` file in the root directory:
     ```shell
     touch .env
     ```
   
   - Go through the `.env.sample` file and add the necessary configurations to the `.env` file.
     
6. Run the application:

   ```shell
   python3 main.py
   ```

7. Run the test:

   ```shell
   python3 integration_test.py && python3 unit_test.py
   ```

### Sample .env

A Fork of Ethereum Sepolia Testnet has been created on Tenderly with initializing the two Ethereum addresses with ERC20 token balances to the run the test simulation on the Forked network.

```cmd
# RPC_NODE_URL=<RPC NODE URL OF THE BLOCKCHAIN NETWORK>
RPC_NODE_URL="https://rpc.tenderly.co/fork/e9488f85-bd1e-4abc-82a1-d863616ef6a0"

# ERC20_TOKEN_ADDRESS=<CONTRACT ADDRESS OF ERC20 TOKEN FOR TOKEN TRANSFER IN CHECKSUM>
ERC20_TOKEN_ADDRESS="0x779877A7B0D9E8603169DdbD7836e478b4624789"

# SOURCE_ADDRESS=<ADDRESS OF SOURCE IN CHECKSUM>
SOURCE_ADDRESS="0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

# RECEIVER_ADDRESS=<ADDRESS OF RECEIVER IN CHECKSUM>
RECEIVER_ADDRESS="0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

# PRIVATE_KEY=<PRIVATE KEY OF THE SOURCE ADDRESS TO PERFORM TOKEN TRANSFERS>
PRIVATE_KEY="ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
```